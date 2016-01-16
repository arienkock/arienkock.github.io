---
title: Should we be making new Databases?
---
At the [2013 edition of the XLDB conference](https://conf-slac.stanford.edu/xldb-2013/) there was an interesting panel discussion called "__Buy vs Build: Why Large Projects Rebuild, Not Reuse?__". Some database engineering big-shots entertained the question whether it is better to adopt and adapt a mechanism for storing data (like SQL, a document store, or simple a distributed file-system for OLAP) or to make a tailored to fit solution. At the [:50 second mark](http://youtu.be/jjrYIRywxok?t=50s) Mike Stonebreaker does a short exposition of the good that happened when the industry collectively decided on SQL. As he puts it:

> Sometimes "good enough" is better than rebuilding.

###Bad Enterprise
Having commercially backed DB vendors is a good thing, right? Yes, it mostly is and I love SQL. It's really good an all the years of development have made it really good at what it does. Time eventually narrows the optimal deployment environment for software. You write more code and you commit more and more to a certain solution space. Being gradually locked in means less room for innovation. Add to this the fact that enterprise solutions more likely to cater to too many wishes, trying to make the most feature-rich product they can. This makes it attractive to anyone reading the brochure, but anyone having to implement the product breaks out in a cold sweat. A jack of all trades is a master of none. A poignant example of enterprise level products seeming to live in a different world than regular people is in the development of OAuth 2.0, which is painfully documented in the article [OAuth 2.0 and the Road to Hell](http://hueniverse.com/2012/07/26/oauth-2-0-and-the-road-to-hell/). 

Also, educational organizations and government are not so eager to adopt closed source software. Even if labeled as open core and/or dual-licensed, it hurts to think about your continuity being in danger. Neo4j, is a sad example of a very cool product, not fully open sourced.

###Being your own best friend
Google makes in-house storage systems in close coordination with their client, which is Google itself.
Jeff Dean mentions it several times in his talk at the same XLDB conference. Here he talks about [knowing the requirements for GFS](http://youtu.be/gCGvneeHbPQ?t=4m20s). In order to do a specific thing better than before sacrifices in functionality need to be made. This means sometimes ignoring your client's request, which is easier if **you** are your own client. It is the opposite of design by committee. It is design by dictatorship.

I believe in the [Benevolent Dictator For Life](http://en.wikipedia.org/wiki/Benevolent_dictator_for_life) system. Sometimes long meetings about the direction of a product or company yield new insights that eventually lead to something good, but most of the time what you really want is a shared vision. If unable to agree on such a vision, a hero must arise. The decider. 

###And yet... fragmentation is bad
Starting over is not so much reinventing the wheel as it is making a version of the wheel that better suits your individual needs, possibly using the **hard-learned** lessons of the wheel-invention process. After millions  invested in wheel technology, you can't expect to **fully** replace it so easily. Mike Stonebreaker is very clear about MapReduce **not being a database** and that it might one day grow up to be one. He's not saying the premise or technology is bad, he's saying it's not **yet** a replacement for commercial parallel RDBMSes.

So full steam ahead on starting new-paradigm projects? If everyone thought that way we would have many not-so-good solutions and no "great" ones. People just like new stuff, datastores are no exception. I like them too, even though I fail to get excited for things like LevelDB and its Node.js binding [LevelUP](https://github.com/rvagg/node-levelup). I'm not saying Hadoop based products are not good. However, if Mike is to be believed, we should be making more progress. If the Hadoop vendors give back to the upstream, then it shouldn't be a problem, but I'm always skeptical of the modern-day free-market, stereotypically looking to cash in on the latest trends. 
