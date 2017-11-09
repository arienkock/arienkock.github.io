---
title: "Modularity Deep Dive - pt. 1"
teaser: Why bother with modules
---

Part 1 | [Part 2](/2017/10/22/Modularity-part2.html)

Why is it so hard to "do the right thing"? It's always easier to insert more code than it is to refactor. First you have to decide what belongs where as you take things apart. Then you have to reimplement all the tests and clean up all the errors that occur as responsibilities move and change. It's both difficult as well as a lot of work. But it's worth it. Sometimes, when I do a good job of it, I get to reuse the component in a new and unforseen way. Those moments make me feel like some sort of genius programmer. I like those moments. That is modularity. 

I wrote this post, because, approximately two years ago something happened. Project Jigsaw was getting a lot of attention and since then I spent a lot of time reading and thinking about modularity. This article isn't about JPMS, but rather modularity as a design concept. In this post I'll talk about:

1. Why do we want to make things modular?
1. What makes a good module?


## Research

I was born in '82 and as a student I didn't do a lot of extracurricular reading. For a long time I've been unaware of a lot of the academic history of computer science. Thankfully, I watch a lot of YouTube. I came across a video of **GOTO conf 2016** where at [minute 34](https://youtu.be/r18BaOHRpE8?t=34m43s) the host seems to call me out personally for never having read [David L. Parnas'](https://en.wikipedia.org/wiki/David_Parnas) work on modularity. So, I did. 
 
The take-away from the paper "[On the Criteria To Be Used in Decomposing Systems into Modules](https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf)", as the title suggests, is a criterion. A *rule* that tells you where to draw the lines when you draw those boxes on paper. You know, those boxes that only vaguely map to the actual code you end up writing? The rule, Parnas concludes, is to **modularize around difficult design decisions**. For example: how do we store our data? Are we sure? How likely is it to change? Let's *abstract it*. Our data storage and schema is now abstracted into a module that hides the details. If done well, it makes it easier to change later. At the same time, it makes concrete what our requirements are. This rule sounds awfully familiar. I must have heard it somewhere else on YouTube.

It sounds a lot like [Robert Martin on Clean Architecture](https://youtu.be/Nsjsiz2A9mg?t=56m31s). Both Parnas' paper and Clean Architecture highlight something important about software design. The reason why we need to create modules is to postpone decisions, which gives us **future agility**. Or as Bob puts it: 

> "Later is always better when you're making decisions; you have more information later." 

Using "decision deferment" as a guiding principle produces a different delineation of modules than the one of "steps in a data processing pipeline". Knowing this certainly does not make it an easy thing to do. Thinking through it takes time. Time not spent writing code, which can feel or look unproductive. On the upside, it can save you long discussions about the choice of technology and futile attempts at predicting far into the future. Another benefit is that modules that can change independently, can also change simultaneously. Leading to efficient parallel development.

## Conclusion

The answer to the first question "Why write modular code?" is: *In order to remain agile*. Had you asked me two years ago, I might have said something about *reusability*. But that is a feature of how they are implemented, not the reason why we made them in the first place. Being agile is easy in the beginning, because you have no other code. Staying agile takes deliberate and careful design. Now the answer to the second question "What makes a good module?" seems pretty obvious: *One that makes future change easy*. I believe modules can do these things. But only when we, the programmers, choose a direction up front.

Part 1 | [Part 2](/2017/10/22/Modularity-part2.html)