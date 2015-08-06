---
published: true
layout: post
---




I used to think interfaces were a premature abstraction. In other words: something you did so that you could migrate or switch implementations/providers in some not so probable future. In all my software engineering classes the true value of decoupling was never explained to me in such a way that it made me a believer. After an unpleasant experience programming against interfaces as a junior programmer I found them quite distasteful.

## DAI & DAO
I was 25 years old and I had just started my first job as a developer. When I opened up my IDE and explored the codebase, I came across the data-access layer of the code. "Data Access Interfaces" (DAI's) and "Data Access Objects" (DAO's), you say? Well, I guess that makes sense. After all, I remember my professors saying it was good to separate the public API from the implementation. A few months in I wasn't so convinced. The DAO's were ever changing and evolving. I wasn't as comfortable with my IDE at the time, so all this jumping back and forth between interfaces and implementations, keeping them up to date as you "tried stuff out" was a real pain in the ass. The number DAI/DAO's was growing and I couldn't make sense of what purpose they served. The DAO implementations were *right there*! I could cast down to them or use them directly, and why wouldn't I?

I asked my senior colleague to explain this to me and he unintentionally struck another blow to my already damaged faith in interfaces. He said 
> "Well, what if we ever want to replace the persistence code with something else. Then we wouldn't have to rewrite all the other classes that only know about the DAI's."

I wasn't satisfied with that! We were not exercising any constraint while changing the DAI's. That's going to be a hell of a migration if that ever happens. Would that ever happen? (It wasn't, it turns out.) Was it worth the time invested in maintaining the interfaces? Also, if we didn't use interfaces and we DID have to migrate, couldn't we just make the DAO's into interfaces then sweep up the implementation from under it?

So was the young naive me wrong? The DAI's were a form of decoupling, and that's good, right? When I think back now I realise it was bit more complicated than that. It's a question of design and architecture.

## 7 years later
The true value of interfaces became clear to me over time. I wish I could point to a single event where it "clicked", but I can't for the life of me think of one such moment. Interfaces *are* about decoupling, but *where* we decouple is important. Where we draw our lines is informed by *why* we decouple. Reasons like maintainability, composability etc. Choosing these places to separate responsibilities takes careful consideration.

I'm currently refactoring a relatively young project. I'm trying to split up the code according to [the clean architecture](https://blog.8thlight.com/uncle-bob/2012/08/13/the-clean-architecture.html) and the dependency rule. If your code is all contained in one software bundle, then there is no stopping any piece of code from talking to the other. There is a giant pitfall for a developer of simply bypassing the *correct* component, assuming there is one. If you decided to forgo structuring your code into components, as you might when just starting out, then there is not even a *hint* in the code to let a developer know that they're spaghettifying the application. However, once you decide on what a component is and what its contract with the outside world is, sticking to it is your only weapon against the [increasing entropy of your design](http://martinfowler.com/articles/designDead.html). Sticking to self-imposed rules takes discipline, and that's not something everyone is blessed with.

When you separate concerns you can do so in varying degrees. Part of the way: Introduce a naming convention or namespaces. All the way: make any code that is not part of the public interface invisible or otherwise unreachable from the other modules. When going the second route, you're making it so hard to do the wrong thing that anyone trying to screw up would have to make an effort. I'm a strong believer in making the "right thing" easier to do than the wrong thing (a.k.a. [falling into the pit of success](http://blog.codinghorror.com/falling-into-the-pit-of-success/)). Applying this whenever you design an API or in the case of code: project structure. Interfaces are one of several tools you can use to achieve this. However, if you leave it at simply *having* interfaces, it can be hard to understand why they're there. If it's clear that they represent a boundary, because they are opaque, then respecting that boundary becomes easy because it's necessary. As a result, you'll write cleaner code.
