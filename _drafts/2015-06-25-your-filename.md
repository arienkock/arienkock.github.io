---
published: false
---

## Misunderstanding Interfaces
I used to think interfaces were a premature abstraction, i.e. something you did so that you could migrate or switch implementations/providers in some in the not so probable future. In all my software engineering classes the true value of decoupling was never conveyed to me in such a way that it made me a believer. Add to that my first professional encounter programming against interfaces and at some point I found them quite distasteful.

## DAI & DAO
I was 25 years old and I had just started my first job as a developer. When I opened up my IDE and explored the code base I came across the data-access layer of the code. "Data Access Interfaces" (DAI's) and "Data Access Objects" (DAO's), you say? Well, I guess that makes sense. After all, my professors said it was good to separate the public API from the implementation. I wasn't so positive a few months in. The DAO's were ever-changing and ever-evolving. I wasn't as comfortable with my IDE at the time, so all this jumping back and forth between interfaces and implementations, keeping them up to date as you "tried stuff out". The number DAI/DAO's was growing and I couldn't make sense of what purpose they served. The DAO implementations were *right there*! I could cast down to them or use them directly, and why wouldn't I?

I asked my senior colleague to explain this to me and he unintentionally struck another blow to my already damaged faith in interfaces. He said 
> "Well, what if we ever want to replace the DAO's with something else. Then we wouldn't have to rewrite all the other classes that only know about the DAI's."

Unsatisfactory! We were not exercising any constraint while changing the DAI's. That's going to be a hell of a migration if that ever happens. Would that ever happen? It wasn't, it turns out. Was it worth the time invested in maintaining the interfaces? Also, if we didn't use interfaces and we DID have to migrate, couldn't we just make the DAO's into interfaces then sweep up the implementation from under it?

Is that any different from the how they were used in the DAI <-> DAO example? That was also decoupling, but it was a leaky one. The persistence strategy seeped through the interfaces. Besides that, the DAI's were used in all other layers of the application. Thirdly, when we had a new data requirement we just added onto the growing number of public methods in our API. It only added to the maintenance and we seemed to gain nothing for it.

## 7 years later
The true value of interfaces became clear to me over time. I wish I could point to a single event where it "clicked", but I can't for the life of me think of one such moment. Interfaces are about decoupling. I'm currently refactoring a relatively young project. I'm trying to split up the code according to [the clean architecture](https://blog.8thlight.com/uncle-bob/2012/08/13/the-clean-architecture.html) and the dependency rule. If your code is all contained in one software bundle, then there is no stopping any piece of code from talking to the other. There is a giant pitfall for a developer of simply bypass the interface, assuming there is one. If not then there is not even a hint in the code to let a developer know that they're spaghetiifying your application.

When you separate concerns you can go part of the way or all the way. Part of the way: Introduce a naming convention or namespaces. All the way: make any code that is not part of the public interface invisible or otherwise unreachable from the other modules. Going the second route you're making it so hard to do the wrong thing that anyone trying to screw up would have to make an effort. I'm a strong believer in making the "right thing" easier to do than the wrong thing. Also referred to as [falling into the pit of success](http://blog.codinghorror.com/falling-into-the-pit-of-success/).