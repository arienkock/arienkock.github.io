---
title: Please use SPDY in your webapps
---
_As SPDY has been superceded by HTTP/2, you can consider this post outdated._

I hope you've heard about the SPDY protocol. I "discovered" it only a half a year ago reading Jetty's documentation which proudly announced supporting it. Since then... I've become a believer/advocate. With SPDY support finally landing in Safari 8, a large number of people can **potentially** benefit from the improved page loading times it promises. However, at smaller scales it's not as well-supported (**citation needed**), but pretty much all of Google's web servers support it as well as most large CDN's.

### What does SPDY do?
It speeds up page loads by allowing multiple resources to be sent across a single connection. More so than a persistent connection, because it multiplexes/interleaves bytes/frames so that multiple resources can be requested and received __'simultaneously'__. Read the [SPDY whitepaper](http://dev.chromium.org/spdy/spdy-whitepaper) for more details.

In addition to this it supports the pushing of resources by the server ahead of the client's realizing it needs them. Keep in mind that this is probably the biggest game-changer of SPDY. Before a browser can parse the HTML and figure out what stylesheets, scripts, and images it needs, it could already be receiving the data. By the time it figures out the HTML, there could be no more requests left to be made!


### SPDY support
When Safari 8 becomes the current version, [SPDY will be supported across the board](http://caniuse.com/#feat=spdy) for all 'major browsers' (which at the time of this writing is not yet the case).

What about web servers, you ask? I feel like I'm simply quoting the [Wikipedia SPDY page](http://en.wikipedia.org/wiki/SPDY), but it's supported in Apache (by a [module implemented by Google itself](https://code.google.com/p/mod-spdy/)), Nginx and [node.js](https://github.com/indutny/node-spdy). What's not on there is that apparently [you can use SPDY in a Go server](https://godoc.org/code.google.com/p/go.net/spdy) and [Tomcat has experimental support](http://www.theserverside.com/news/thread.tss?thread_id=76803). Since many sites use either Apache HTTPd or Nginx as a proxy to their application server, there isn't really much stopping anyone from getting SPDY.

### Getting started: Requirements
To start, you can: 

1. Grab a Jetty 9 distribution and use the SPDY config, or
2. setup Apache with `mod_spdy` or [`mod_pagespeed`, which supports SPDY almost automatically](https://developers.google.com/speed/pagespeed/module/https_support).
3. There is an alternate scenario if you use static pages with a RESTful API as a backend (which is often the case in single page apps). You could offload ALL your content to a CDN like Cloudflare and benefit from their SPDY support without writing a single line of SPDY-enabling configuration.

What else you'll need:

1. You need a valid certificate obviously, because SSL is required to use SPDY transparently.
2. Your resources need to be on the same server as your application (assuming the HTML is application generated and not static).
3. Logic that connects resources to enable SPDY Push. In case of Jetty, there is a component which auto-detects and remembers these relationships ([`ReferrerPushStrategy`](http://www.eclipse.org/jetty/documentation/current/spdy-implementing-push.html)). In `mod_spdy` you work with a header passed by the backend that lists the `X-Associated-Content`, which allows the module to pre-fetch the content from the server it's proxying and push it to the client.

### The down side of SPDY Push
Imagine you've set all this up and you are amazed at the precognition of your web-page loads. You now realize you're pushing resources to users that may already have locally cached versions. You're sending useless duplicate bytes over the line. It may at first seem like acceptable collateral damage, but you're a good developer and this itch needs to be scratched. So instead, you want to: __Push on first view only__.

To accomplish this you need to remember a user's visit, e.g. set a session cookie with a value identifying the page, or better yet the set of resources belonging together. The same can be done with a server side session, but it's nice to offload this state onto the client if you want to improve performance by not having sessions in the first place. In both cases you need to write this code yourself, because at this time neither Jetty's bundled PushStrategy nor mod_spdy support this type of behaviour.

### In conclusion
Now that Google makes SSL support a variable in your PageRank, most people have started serving their sites securely for this reason. Though it may not be the most noble of motivations, it's a step in the right direction. Any CDN worth their salt will support serving your content over SSL on your own domain, even though this probably means buying a certificate through them from which they benefit. This takes care of our first requirement. What's left is a bit of time invested by us, the developers, to make the web a ~~better~~ faster place.
