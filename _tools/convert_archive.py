#!/usr/bin/env python3
"""
One-shot converter: walks year-directories (2013..2018), extracts the
<div class="article">...</div> body from each old HTML post, converts it to
Markdown, and writes a Jekyll collection file to _archive/.

Also scrapes the old index.html to pick up the teaser-line for each post so
that we can use it as a `subtitle` in the front-matter.

Run from the repo root:  python3 _tools/convert_archive.py
"""

from __future__ import annotations
import os
import re
import html as htmllib
from pathlib import Path
from html.parser import HTMLParser
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
LEGACY_ROOT = ROOT / "legacy"
YEARS = ["2013", "2014", "2015", "2016", "2017", "2018"]
ARCHIVE_DIR = ROOT / "_archive"
LEGACY_INDEX = LEGACY_ROOT / "old-index.html"


# ---------------------------------------------------------------------------
# Slurp subtitles out of the old index.html (already moved to legacy/)
# ---------------------------------------------------------------------------
def load_subtitles(index_html: str) -> dict[str, str]:
    """Returns { slug.html : teaser-line }. Slug is the basename of the post URL."""
    subs: dict[str, str] = {}
    pattern = re.compile(
        r'<a href="/\d{4}/\d{2}/\d{2}/([^"]+\.html)">\s*'
        r'<div class="date">[^<]+</div>\s*'
        r'<h2 class="item-title">[^<]+</h2>\s*'
        r'<div class="teaser-line">([^<]+)</div>',
        re.S,
    )
    for m in pattern.finditer(index_html):
        slug, teaser = m.group(1), htmllib.unescape(m.group(2)).strip()
        subs[slug] = teaser
    return subs


# ---------------------------------------------------------------------------
# Extract the <div class="article"> inner HTML and the <h1 class="articleTitle">
# ---------------------------------------------------------------------------
class ArticleExtractor(HTMLParser):
    """Extract <div class="article"> innerHTML. Track div-nesting with a stack of
    classes so we can cleanly exit the article wrapper and skip elements like
    <div class="posted-on-date">...</div> wholesale.
    """

    VOID = {"br", "hr", "img", "input", "meta", "link"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.in_article = False
        self.title: str | None = None
        self._capture_title = False
        self._title_buf: list[str] = []
        self._html_buf: list[str] = []
        # Stack of open div classes while inside the article. Used to find the
        # article's own closing </div>.
        self._div_stack: list[str] = []
        # Depth of nested elements we are currently dropping (e.g. posted-on-date).
        self._skip_depth = 0

    # --- helpers ----------------------------------------------------------
    def _attrs_str(self, attrs) -> str:
        return "".join(
            f' {k}="{htmllib.escape(v or "", quote=True)}"' for k, v in attrs
        )

    def _emit(self, s: str) -> None:
        if self.in_article and not self._capture_title and self._skip_depth == 0:
            self._html_buf.append(s)

    # --- tag handlers -----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        cls = attr_dict.get("class", "")
        classes = cls.split()

        # Before we're inside the article, look for the opener.
        if not self.in_article:
            if tag == "div" and "article" in classes:
                self.in_article = True
                self._div_stack.append("article")
            return

        # Already inside article:
        # Title capture
        if tag == "h1" and "articleTitle" in classes:
            self._capture_title = True
            return

        # Track div nesting so we can find the article's closing </div>.
        if tag == "div":
            self._div_stack.append(cls)
            # Start skipping if this is the posted-on-date wrapper
            if "posted-on-date" in classes and self._skip_depth == 0:
                self._skip_depth = 1
                return
            if self._skip_depth > 0:
                self._skip_depth += 1
                return

        if self._skip_depth > 0:
            if tag not in self.VOID:
                self._skip_depth += 1
            return

        slash = " /" if tag in self.VOID else ""
        self._emit(f"<{tag}{self._attrs_str(attrs)}{slash}>")

    def handle_endtag(self, tag):
        if not self.in_article:
            return

        if self._capture_title and tag == "h1":
            self._capture_title = False
            self.title = htmllib.unescape("".join(self._title_buf)).strip()
            return

        if tag == "div":
            # Pop the matching open div
            if self._div_stack:
                popped = self._div_stack.pop()
            else:
                popped = ""
            if self._skip_depth > 0:
                self._skip_depth -= 1
                return
            if not self._div_stack:
                # closed the outer article div
                self.in_article = False
                return
            # fall through to emit </div>
            self._emit("</div>")
            return

        if self._skip_depth > 0:
            if tag not in self.VOID:
                self._skip_depth -= 1
            return

        if tag not in self.VOID:
            self._emit(f"</{tag}>")

    def handle_startendtag(self, tag, attrs):
        if not self.in_article or self._capture_title or self._skip_depth > 0:
            return
        self._emit(f"<{tag}{self._attrs_str(attrs)} />")

    def handle_data(self, data):
        if self._capture_title:
            self._title_buf.append(data)
        else:
            self._emit(data)

    def handle_entityref(self, name):
        s = f"&{name};"
        if self._capture_title:
            self._title_buf.append(s)
        else:
            self._emit(s)

    def handle_charref(self, name):
        s = f"&#{name};"
        if self._capture_title:
            self._title_buf.append(s)
        else:
            self._emit(s)

    @property
    def html(self) -> str:
        return "".join(self._html_buf).strip()


# ---------------------------------------------------------------------------
# HTML → Markdown conversion (tailored to the small tag set used in these posts)
# ---------------------------------------------------------------------------
class HtmlToMarkdown(HTMLParser):
    """A pragmatic converter handling the tags actually found in these posts:
    p, h1-h6, blockquote, ul/ol/li, pre/code (no inner tags), a, strong/b,
    em/i, img, br, hr, span, div (transparent).
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.stack: list[str] = []
        self.list_stack: list[tuple[str, int]] = []  # (ul/ol, item counter)
        self.in_pre = 0
        self.in_code_inline = 0
        self.link_stack: list[str] = []
        self.link_text_buf: list[list[str]] = []  # per-link text buffers
        self.pre_lang: list[str] = []

    # --- helpers ---------------------------------------------------------
    def _write(self, s: str) -> None:
        # If we are inside an <a>, capture into the link buffer.
        if self.link_text_buf:
            self.link_text_buf[-1].append(s)
        else:
            self.out.append(s)

    def _nl(self, n: int = 1) -> None:
        self._write("\n" * n)

    def _list_prefix(self) -> str:
        parts = []
        for i, (kind, counter) in enumerate(self.list_stack):
            if i < len(self.list_stack) - 1:
                parts.append("    ")
        kind, counter = self.list_stack[-1]
        marker = "-" if kind == "ul" else f"{counter}."
        return "".join(parts) + marker + " "

    # --- tag handlers ----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)

        if tag == "p":
            self._nl(2)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            # Demote one level: old h1 inside article becomes H2 here (we render a site H1).
            level = int(tag[1])
            # All old headings were already below the post title H1; keep them.
            self._nl(2)
            self._write("#" * level + " ")
            self.stack.append(tag)
        elif tag == "blockquote":
            self._nl(2)
            self.stack.append("blockquote")
        elif tag == "ul":
            self.list_stack.append(("ul", 0))
            self._nl(1 if self.list_stack else 2)
        elif tag == "ol":
            self.list_stack.append(("ol", 0))
            self._nl(1 if self.list_stack else 2)
        elif tag == "li":
            if self.list_stack:
                kind, counter = self.list_stack[-1]
                self.list_stack[-1] = (kind, counter + 1)
            self._nl(1)
            self._write(self._list_prefix())
        elif tag == "pre":
            self.in_pre += 1
            self._nl(2)
            self._write("```")
            # Detect language from class on pre or nested code
            cls = attr.get("class", "")
            lang = ""
            m = re.search(r"(?:^|\s)(?:lang-|language-)([\w+-]+)", cls)
            if m:
                lang = m.group(1)
            self.pre_lang.append(lang)
            self._write(lang + "\n")
        elif tag == "code":
            if self.in_pre:
                # capture language from code class if pre didn't have one
                if self.pre_lang and not self.pre_lang[-1]:
                    cls = attr.get("class", "")
                    m = re.search(r"(?:^|\s)(?:lang-|language-)([\w+-]+)", cls)
                    if m:
                        # rewrite previous ```\n to include lang
                        lang = m.group(1)
                        # Find the last '```\n' we emitted and update
                        for i in range(len(self.out) - 1, -1, -1):
                            if self.out[i] == "```" or (
                                self.out[i].startswith("```")
                                and self.out[i].endswith("\n")
                            ):
                                self.out[i] = (
                                    f"```{lang}\n"
                                    if self.out[i].endswith("\n")
                                    else "```"
                                )
                                break
                        self.pre_lang[-1] = lang
            else:
                self.in_code_inline += 1
                self._write("`")
        elif tag in {"strong", "b"}:
            self._write("**")
        elif tag in {"em", "i"}:
            self._write("_")
        elif tag == "a":
            href = attr.get("href", "")
            self.link_stack.append(href)
            self.link_text_buf.append([])
        elif tag == "img":
            src = attr.get("src", "")
            alt = attr.get("alt", "")
            self._write(f"![{alt}]({src})")
        elif tag == "br":
            if self.in_pre:
                self._write("\n")
            else:
                self._write("  \n")
        elif tag == "hr":
            self._nl(2)
            self._write("---")
            self._nl(2)
        # span / div / sup / sub / ... — transparent passthrough for text

    def handle_endtag(self, tag):
        if tag == "p":
            self._nl(1)
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._nl(1)
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
        elif tag == "blockquote":
            if self.stack and self.stack[-1] == "blockquote":
                self.stack.pop()
            self._nl(1)
        elif tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            self._nl(1)
        elif tag == "li":
            pass
        elif tag == "pre":
            if self.in_pre:
                self.in_pre -= 1
            # Ensure a newline before the closing fence
            if self.out and not self.out[-1].endswith("\n"):
                self._write("\n")
            self._write("```")
            self._nl(2)
            if self.pre_lang:
                self.pre_lang.pop()
        elif tag == "code":
            if self.in_pre:
                pass
            else:
                if self.in_code_inline:
                    self.in_code_inline -= 1
                self._write("`")
        elif tag in {"strong", "b"}:
            self._write("**")
        elif tag in {"em", "i"}:
            self._write("_")
        elif tag == "a":
            href = self.link_stack.pop() if self.link_stack else ""
            text_parts = self.link_text_buf.pop()
            text = "".join(text_parts).strip()
            # Fall back to the href if no text
            if not text:
                text = href
            self._write(f"[{text}]({href})")

    def handle_data(self, data):
        if self.in_pre:
            self._write(data)
            return

        # Inside a blockquote: we'll convert to "> " line-prefixes at the end.
        # For now, just emit raw text; prefixing happens in post-process.
        self._write(data)

    # -------------------------------------------------------------------
    def result(self) -> str:
        md = "".join(self.out)

        # Collapse 3+ blank lines to 2
        md = re.sub(r"\n{3,}", "\n\n", md)

        # Blockquote handling: we didn't track it strictly, so instead we
        # post-process by re-running the input through a second pass.
        # (The first pass leaves blockquote content as normal paragraphs.)
        return md.strip() + "\n"


def rewrite_internal_links(html: str) -> str:
    """Rewrite links to old post URLs so they point to the new archive path.

    /YYYY/MM/DD/slug.html[#frag]  →  /archive/YYYY-MM-DD-<slugified>/[#frag]
    """
    pattern = re.compile(r'(href=")(/\d{4}/\d{2}/\d{2}/)([^"#]+)\.html(#[^"]*)?(")')

    def _sub(m: re.Match) -> str:
        prefix = m.group(1)
        datepath = m.group(2)  # /YYYY/MM/DD/
        fname = m.group(3)  # slug (may have mixed case)
        frag = m.group(4) or ""
        tail = m.group(5)
        # Build YYYY-MM-DD from datepath
        y, mo, d = datepath.strip("/").split("/")
        new_slug = slugify(fname + ".html")
        return f"{prefix}/archive/{y}-{mo}-{d}-{new_slug}/{frag}{tail}"

    return pattern.sub(_sub, html)


def html_to_markdown_with_blockquotes(html: str) -> str:
    """Wraps HtmlToMarkdown with a pre-processing pass that converts
    <blockquote>...</blockquote> blocks to '> ' prefixed Markdown blocks.

    We do it with a regex because blockquotes in these posts always contain
    only <p> and inline elements, and they are never nested.
    """

    def repl(m: re.Match) -> str:
        inner = m.group(1)
        # Convert the inner to markdown first
        conv = HtmlToMarkdown()
        conv.feed(inner)
        inner_md = conv.result().strip()
        # Prefix every line with "> "
        lines = inner_md.splitlines() or [""]
        quoted = "\n".join("> " + line if line.strip() else ">" for line in lines)
        return "\n\n" + quoted + "\n\n"

    # Non-greedy match for blockquotes
    html2 = re.sub(
        r"<blockquote[^>]*>(.*?)</blockquote>", repl, html, flags=re.S | re.I
    )

    conv = HtmlToMarkdown()
    conv.feed(html2)
    return conv.result()


# ---------------------------------------------------------------------------
# Filename helpers
# ---------------------------------------------------------------------------
def slugify(name: str) -> str:
    name = name.lower()
    # Strip .html
    if name.endswith(".html"):
        name = name[:-5]
    # Keep alphanumerics and dashes
    name = re.sub(r"[^\w-]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def yaml_escape(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{s}"'


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    ARCHIVE_DIR.mkdir(exist_ok=True)

    # Read subtitles from the preserved old index
    subtitles: dict[str, str] = {}
    if LEGACY_INDEX.exists():
        subtitles = load_subtitles(LEGACY_INDEX.read_text(encoding="utf-8"))

    total = 0
    for year in YEARS:
        yd = LEGACY_ROOT / year
        if not yd.exists():
            continue
        for html_path in sorted(yd.rglob("*.html")):
            # Expected layout: legacy/year/MM/DD/slug.html
            try:
                rel = html_path.relative_to(LEGACY_ROOT)
                parts = rel.parts  # (year, month, day, file)
                y, m, d, fname = parts[0], parts[1], parts[2], parts[3]
                post_date = date(int(y), int(m), int(d))
            except Exception as e:
                print(f"skip (bad path): {html_path} — {e}")
                continue

            raw = html_path.read_text(encoding="utf-8", errors="replace")

            extractor = ArticleExtractor()
            extractor.feed(raw)
            title = extractor.title or fname.replace(".html", "").replace("-", " ")
            body_html = extractor.html

            if not body_html.strip():
                print(f"warn: empty body, skipping: {html_path}")
                continue

            body_html = rewrite_internal_links(body_html)
            body_md = html_to_markdown_with_blockquotes(body_html)

            # Tidy: collapse 3+ blank lines, trim leading newlines.
            body_md = re.sub(r"\n{3,}", "\n\n", body_md).lstrip("\n")

            slug = slugify(fname)
            subtitle = subtitles.get(fname, "")

            out_name = f"{post_date.isoformat()}-{slug}.md"
            out_path = ARCHIVE_DIR / out_name

            fm_lines = [
                "---",
                f"title: {yaml_escape(title)}",
            ]
            if subtitle:
                fm_lines.append(f"subtitle: {yaml_escape(subtitle)}")
            fm_lines += [
                f"date: {post_date.isoformat()}",
                f"original_url: /{y}/{m}/{d}/{fname}",
                "---",
                "",
            ]

            out_path.write_text("\n".join(fm_lines) + body_md, encoding="utf-8")
            total += 1
            print(f"wrote {out_path.relative_to(ROOT)}")

    print(f"\nConverted {total} posts → {ARCHIVE_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
