#!/usr/bin/env bash
# Downloads external images referenced in _posts/*.md and rewrites the URLs to local /images/ paths.
set -euo pipefail

POSTS_DIR="$(cd "$(dirname "$0")/../_posts" && pwd)"
IMAGES_DIR="$(cd "$(dirname "$0")/../images" && pwd)"

grep -rn '!\[.*\](https\?://' "$POSTS_DIR" --include='*.md' -h | \
  grep -oP 'https?://[^\)]+' | sort -u | \
while read -r url; do
  filename=$(basename "$url" | tr '?' '_' | tr '&' '_')
  dest="$IMAGES_DIR/$filename"
  echo "Downloading $url -> images/$filename"
  curl -fsSL "$url" -o "$dest"
  grep -rl "$url" "$POSTS_DIR" --include='*.md' | \
    xargs sed -i "s|$url|/images/$filename|g"
done

echo "Done. Stage and commit images/ and _posts/ to persist the changes."
