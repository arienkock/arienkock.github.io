---
title: "Modularity Deep Dive - pt. 2"
teaser: modules and your process
---

[Part 1](/2017/09/03/Modularity-part1.html) | Part 2

# Modules and Methodology
The better a module boundary is defined, the fewer modules are affected by changes to your system. This lets different people work on parts of the system at the same time, while being isolated from each other. 

Adding new members to a team does not make them faster or more effective, *unless* they can collaborate well enough to compensate for the increased overhead. 

Modules that are drawn up ahead of time (the best time), are defined with incomplete information. When you notice a trend of cross-cutting concerns, then it's time to redraw the boxes. But what do you do when there is a team who's responsible for a module? What if that module no longer exists after the refactor?

A company can increase the number of developers, but somewhere there is an inflection point. The more thoughtful and deliberate you are about defining responsibilities (for both people and code) the further you can push the size of your team. Get too fixated on those boundaries and you've missed the point. The separation of concerns is to enable change. How the separation happened may turn out to be wrong, and you have to be able to change that.

Modularity is working when it allows parallel development. When that stops being the case, it's time to have a chat. It's easy to recognize those moments of friction inside an organization. Because, you start sensing this misalignment. You notice a conflict of interests, when you should all be working towards the same goal. Someone might misbehave and now it's personal. My team, my poduct, my service... pride gets attached to the wrong thing and now there's *actual* conflict. Good luck fixing that.

Places where this happens often:

1. where front end meets back end
1. where dev meets ops
1. where visual design meets front end
1. where marketing meets dev
1. where HR meets everyone else

It shouldn't come as a surprise that developers have a developer-centric view of the world. It's a question of empathy, that determines how we interact with someone outside of our tribe. It's especially obvious when we depend on someone that doesn't need anything from us. Operations needs to keep servers up. Devs need to push changes, and for that they need ops. What does ops need dev for? Unless you align the values, there will be friction. 

Organizational modularity is about defining contracts. We can negotiate contracts, but they must be able to change. When we notice too many cross-cutting changes in code, we redraw the boxes and the lines. When we notice too much micro-management, too much push-back from ops, too many ad-hoc features from marketing, we generally don't take a step back to change things. And by we I mean people in general. A corporate environment is hierarchical, but relatively static across time. If we discover a deficiency, reorganizing is seen as this epic change imposed from the top down. Meanwhile, people on the front-line of these points of friction would have liked to have seen a small-scale change delivered sooner. In other words, organizational agility.


## Properties of a module
I think it's safe to assume that anyone reading this article has a solid understanding of what a module is. So this chapter is meant to shed new light on your definition by looking at it from different angles. 

### My definition
Let's begin with the definition I've whittled down for myself:

> A software module is a collection of code with a public interface

I leave out words like coupling, reusability and anything else that is the consequence of modularity and not essential. A badly drawn up module is still a module. So I want to separate the virtues from the form. Secondly, note that there's also no mention of any private code. There might be some, there might be none. Yet the word `public` implies that there is some sort of implied/expected access pattern. This might be true access restriction, or simply a convention. My defintion aims to highlight that a module (in software) can take many shapes (a service, `jar` file, package, or class) and that there is some contract which may not be obvious from the code alone. Modularity applies to all scopes.

### Googling it
We can also ask Google for a definition. When you do you get a very elegant answer that applies to IKEA as much as it does to code:

> module: each of a set of standardized parts or independent units that can be used to construct a more complex structure, such as an item of furniture or a building.

This definition shows modules as building blocks. Their primary purpose is to be part of something bigger. And yet, they're independent. Meaning that they stand alone and can potentially be useful on their own.

### Modularity in other disciplines
Next, I'll steal [Rich Hickey's idea](https://www.infoq.com/presentations/Design-Composition-Performance) to look at hardware modularity in synthesizers:

<img src="/images/Modular_synth_2,_Conway_Hall,_2011-06-18.jpg" style="max-width: 100%"/>

This highlights an aspect of modularity that rarely applies to code I write. However, it *does* apply to libraries. Can you guess what I'm talking about? It is the uniformity of the connecting parts. Synth modules can be composed with cables, which means they can be very easily recomposed into different configurations. This topic deserves a chapter of its own.

### Composition
What's the equivalent of cables and electricity in software? Functions and data. While functions and data seem like the lingua franca of software modules, composition is not as straight-forward in code as it is with audio synths. I can make novel sounds with a new wiring of synth modules by simply moving cables around, but almost any composition other than the intended configuration for functions is either nonsensical or simply does not work. Different arguments and return types mean you can't simply compose any two functions. You could make all your functions take and return a map. It's an interesting idea, but there are downsides to it that make it an unlikely solution.

Software modules are not intended (nor expected) to fit together without some glue. You write a program by consuming modules and wiring them up in a useful way. That wiring is a sophisticated program in and of itself, which (unlike the modules it's composed of) is difficult to understand in isolation.

There are ways to limit the complexity of the wiring. One of the first things that this reminds me of is this talk called ["Transducers" by Rich Hickey](https://www.youtube.com/watch?v=6mTbuzafcII). JavaSE's closest out-of-the-box thing to transducers is Streams, but Cognitect provides proper implementations for Java, JS, Ruby, and Python [here](https://github.com/cognitect-labs?utf8=%E2%9C%93&q=transducers&type=&language=). Mr. Hickey is also a fan of [CSP](https://en.wikipedia.org/wiki/Communicating_sequential_processes), which is a programming style I've also become fond of since working in Go. Another way of connecting components without writing too much custom glue is through the use of queues. In Java there are many of these. Java also has Channels, but those don't seem appropriate for program composition. Java as a programming culture/community traditionally doesn't write code that composes this way. My guess is that this is due to Object Orientation. The rise in popularity of Reactive Streams and RX Java may be changing this. However, I don't have sufficient information to say anything definitive beyond observable trends.

### Conclusion
I've started exploring the concepts and motivations behind modularity and it's changed the way I think about writing programs. It's made me more aware of when I'm making design decisions, which turns out to be all the time. It has also made me favor a functional style of programming in order to make (re)composition simpler. Whereas before I tended to model my program as stateful things that interact, this approach forces me to separate data, transformations, and IO ahead of time. Next, I'll go into the problems that are being solved with decomposing software into modules.

Part 1 | [Part 2](/2017/10/22/Modularity-part2.html)



[Part 1](/2017/09/03/Modularity-part1.html) | Part 2