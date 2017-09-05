---
title: "Modularity Deep Dive - pt. 1"
teaser: Why bother with modules
---

I don't like how much work it is to "do the right thing". Most of the time, it's harder to clean up my programs than it is to just insert more stream-of-consciousness code. My most dreaded yet most gratifying refactoring is: moving responsibility from one part of my program to another. "Most dreaded", because it changes the contract of the existing component in a breaking way, cascading changes throughout my program. "Most gratifying", because the component is now smaller, does fewer things and is easier to understand on its own. If I did it right I might even get to reuse the undressed components in new ways, giving me pause to ponder whether I've been a genius all these years without knowing it.
 
 I decided to make a study of modularity when project Jigsaw was first gaining attention, which feels like it was two years ago. Though the details of the JPMS have changed over that period: I was (and still am) by and large unhappy with its implications. The bookkeeping just seems so tedious, and it doesn't even segregate ClassLoaders. This pre-judgement was perhaps a bit unfair. However, this article isn't *about* JPMS in particular. It's about the things I learned while trying to figure out if I (or anyone) really needed such a hard-handed module system .
 
 ## David L. Parnas
 I was born in '82 and as a student I didn't do a lot of extracurricular reading. It often feels like I've missed a lot of the academic history of computer science. Thankfully, I came across [this video of GOTO conf 2016](https://www.youtube.com/watch?v=r18BaOHRpE8) where at [minute 34](https://youtu.be/r18BaOHRpE8?t=34m43s) the host seems to call me out personally for never having read David L. Parnas' papers on modularity. Challenge accepted!
  
  After reading [On the Criteria To Be Used in Decomposing Systems into Modules](https://www.cs.umd.edu/class/spring2003/cmsc838p/Design/criteria.pdf) my initial reaction was luke warm. I often have this problem when coming across good articles or presentations. It took some time to truly sink in, and now I can totally see what I've done wrong in the past.
   
   > "Any sufficiently good advice is indistinguishable from common sense" - Me, just now

The key take away from the paper, as the title suggests, is a rule that tells you where to draw the lines of abstraction. There's still some intuition involved, though. It is worth going through the examples in the paper to better appreciate the conclusion: difficult design decisions are the things you want to hide. How do we store our data? We're not sure yet. It might change. Abstract it! Data storage is now a module with an interface that abstracts away the details.

This sounds a lot like [Robert Martin on Clean Architecture](https://youtu.be/Nsjsiz2A9mg?t=56m31s). There's a story he tells about abstracting away storage details into insignificance. You can keep postponing deciding what database to use and at some point it might just not matter anymore, which saves you the long discussions and futile attempts at predicting the future. What this has in common with Parnas' paper is that the word coupling is nowhere to be found. Modularity doesn't serve the purpose of keeping things loosely coupled, that's the effect and not the goal. The reason why we need to create modules, they say, is not in *order* to hide information, we hide information in order to **gain future agility**. Or as Bob puts it: 

> "Later is always better when you're making decisions; you have more information later." 

This might seem subtle, but using "decision deferment" as a guiding principle produces different program structure. See Parnas' paper for concrete examples.

## What is a Module
It might seem strange to define the word module after the previous chapter. I think doing it this way makes it easier on me, since we've already gotten the "big win" of modules out of the way. There is implicit knowledge that is assumed from someone interested in an article titled "Modularity", but humor me. Let's begin with the definition I want to use in this and future articles:

> A software module is a collection of code with a public interface

Firstly, I leave out words like coupling, reusability and anything else that is the consequence of modularity and not essential. A badly drawn up module is still a module. So I want to separate the virtues from the form. Secondly, note that there's also no mention of any private code. There might be some, there might be none. Yet the word `public` implies that there is some form of implied/expected interaction. This might be true access restriction, but it might also be convention. The JVM has many ways of restricting access and I recommend watching [Confinement in the JVM with John Rose](https://www.youtube.com/watch?v=VPF8DLnDgE4) for an overview which also covers JPMS. These properties of my definition will be more important later, but for now we can also ask Google for a definition. When you do you get a very elegant answer that applies to IKEA as much as it does to code:

> module: each of a set of standardized parts or independent units that can be used to construct a more complex structure, such as an item of furniture or a building.

Next, I'll steal [Rich Hickey's idea](https://www.infoq.com/presentations/Design-Composition-Performance) to look at hardware modularity in synthesizers:

<img src="/images/Modular_synth_2,_Conway_Hall,_2011-06-18.jpg" style="max-width: 100%"/>

Which will hopefully make sense when we look at...

### Composition
Thinking about modules in this way highlights something about software modules that I've generally taken for granted. The uniformity of the connecting parts. Synth modules can be composed with cables, while software composes with functions and data. In Lisps it's even data all the way down. The means by which software modules compose are universal. This insight made me appreciate the importance of FFI, because it enables modularization across programming paradigms. Although, the same could be said for web-services. So "Yes", Microservices are a type of modularity. 

While functions and data seem like the lingua franca of software modules, their composability is not devoid of complications. At least, not inherently. Care must still be taken to avoid pitfalls. Programmers can hamper composability by accepting and returning proprietary data types or mutable data-structures. Fortunately, immutable/persistent data-structures are trending. 


Another aspect of modules is that they not only compose, but compose in many different configurations. This is not as straight-forward in code as it is in other domains. I can make novel sounds with a new wiring of synth modules, but almost any composition other than the intended configuration for software modules is either nonsensical or simply does not work. By that I mean that software modules are not intended (nor expected) to fit together without some glue. You write a program by consuming modules and wiring them up in a useful way. That wiring is a sophisticated program in and of itself, which (unlike the modules it's composed of) is difficult to understand in isolation.

There are ways to limit the complexity of the wiring. One of the first things that this reminds me of is this talk called ["Transducers" by Rich Hickey](https://www.youtube.com/watch?v=6mTbuzafcII). JavaSE's closest out-of-the-box thing to transducers is Streams, but Cognitect provides proper implementations for Java, JS, Ruby, and Python [here](https://github.com/cognitect-labs?utf8=%E2%9C%93&q=transducers&type=&language=). Mr. Hickey is also a fan of [CSP](https://en.wikipedia.org/wiki/Communicating_sequential_processes), which is a programming style I've also become fond of since working in Go. Another way of connecting components without writing too much custom glue is through the use of queues. In Java there are many of these. Java also has Channels, but those don't seem appropriate for program composition. Java as a programming culture/community traditionally doesn't write code that composes this way. My guess is that this is due to Object Orientation. However, the rise in popularity of Reactive programming and RX Java may be changing this. However, I don't have sufficient information to say anything definitive beyond observable trends.

### Conclusion
I've started exploring the concepts and motivations behind modularity and it's changed the way I think about writing programs. It's made me more aware of when I'm making design decisions, which turns out to be all the time. It has also made me favor a functional style of programming in order to make (re)composition simpler. Whereas before I tended to model my program as stateful things that interact, this approach forces me to separate data, transformations, and IO ahead of time. Next, I'll go into the problems that are being solved with decomposing software into modules.
