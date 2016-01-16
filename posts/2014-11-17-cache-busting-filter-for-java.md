---
title: "Cache Busting Filter"
teaser: You may find this useful
---

### TL;DR
1. make a `Filter`
2. rewrite URI's in your pages to contain a hash of your files by wrapping `HttpServletResponse`
3. remove the hash from incoming requests in the same filter 

### The "why?"
This weekend I was looking for a cache-busting solution in the form of a Gulp plugin. Cache busting, in case you're not familiar with the term, is a name for any method of circumventing the (ideally) long time-to-live of cached static resources in web-applications. The simplest of such solutions would be to add a querystring to your js and css URL's each time you update them. The query string has no effect other than to make the browser think the resource is dynamic. However, this breaks in the face of some optimistic CDN's. We need to rename the actual resource file name.

### `gulp-rev` etc.
Many methods exist to accomplish the actual rewriting. Usually as part of the build tool du jour. These have counterparts in the backend code that resolve references inside templates and code to the newly rewritten file names. I found this two-tiered approach to be too involved, since the obvious solution isn't very complicated at all. 

### encodeURL()
At least in Java, where (if you keep to the best-practices) your URL's all pass through [one central piece of code](https://docs.oracle.com/javaee/6/api/javax/servlet/http/HttpServletResponse.html#encodeURL(java.lang.String)). Even if you use Thymeleaf's `@{/style.css}` or JSP's with JSTL `<c:url/>` tags, they all pass through `encodeURL()`.

You can use this feature, which is intended for handling session ID's, to rewrite all your static resource URI's to the hashed equivalent, but that's not all. Since you're able to wrap the response object in a filter, the same filter will also be able to receive the hashed URI from browsers once they try to load your pages. That's our chance to remove the hash from the URI and forward the request to the default handling mechanism of our application container. That will fetch the resource who's real file name hasn't changed at all. So there is no need for build tools to mangle our file names.

### The code
Below is the code, which I documented more than I do most other stuff I write. I use a `CheckedInputStream` to calculate the hash in a streaming fashion.

<script src="https://gist.github.com/arienkock/c0a236aad1ed7e31f134.js"></script>

Thanks to @eranievs for pointing out a bug in the implementation. The filter didn't work with non-root context paths. The Gist has been updated.

<blockquote class="twitter-tweet" lang="en"><p lang="en" dir="ltr"><a href="https://twitter.com/ArenCawk">@ArenCawk</a> Using your Cache Busting Filter, but running into some issues. <a href="http://t.co/Y6exo4VEsc">http://t.co/Y6exo4VEsc</a></p>&mdash; Svein Are (@eranievs) <a href="https://twitter.com/eranievs/status/595511122066804736">May 5, 2015</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>