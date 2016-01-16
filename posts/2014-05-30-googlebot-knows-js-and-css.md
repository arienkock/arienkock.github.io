---
title: Googlebot Knows JS and CSS
teaser: and it's not a valid excuse
---
A week ago Google came out with [big news](http://googlewebmastercentral.blogspot.co.uk/2014/05/understanding-web-pages-better.html). Now all your single page apps get indexed properly without a static page fallback. Pages that rely on `pushState` for navigation used to have to do extra work to [make their sites indexable](https://support.google.com/webmasters/answer/174992?hl=en).

### The good###
Google being the gods of search and by extension the masters to which all of e-commerce caters, is now saying that they can better handle your complex webapps. You can use Ajax calls from the get-go and not pay a hefty price. This makes development simpler and that is good. 

No longer can you hide away content and pretend like it's part of your page as part of some SEO scheme. With CSS being rendered, the visual position and thus the relevance of content can be more accurately judged by Google's indexing mechanism. This means better search results and this is even better.

### The bad
I think the best developers are lazy developers. By that I mean that a lazy developer will do a repetitive task only a few times before automating it. The essence of good code is reusability. However, there is also a bad kind of lazy. The lazy developer that is __TOO__ lazy to automate will forego the chance to make a generic solution in favor of a less sophisticated solution. The promise being that he won't have to do that exact task again __him-/herself__ or that the burden of maintenance will fall on the shoulders of someone else or, best of all, no one at all. If you __can__ hack together a page with asynchronous calls with existing services doesn't mean you __should__. The goal of maintainability and performance suffers in the face of ad-hoc solutions. This is bad.

As mobile devices get more powerful they can bear a heavier processing load than before. You can create more complex interfaces that improve the UX aspect of a webapp. That's great as long as that's the actual reason. Why would a page __NOT__ load the main content in the first request? Now you can argue that if it's fast enough, it doesn't matter, because Google said so. They didn't, actually, if you read that article, they suggest you degrade gracefully. Google and humans are not the only consumers on the web. There are other bots, applications and not all of them can fetch using a headless browser like [PhantomJs](http://phantomjs.org/). Google can't process pages as fast with client side rendering as they could before and most other parties definitely can't.

### Don't change too much
I like the idea of not needing to create a static version of a page for SEO purposes only. Heck, I think it's just swell. However, if the future of the internet consists of pages that need 5+ requests before it's usable, then someone has failed somewhere along the line.
