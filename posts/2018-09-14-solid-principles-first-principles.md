---
title: "SOLID Principles to First Principles"
teaser: a teaching experiment at a WebDev bootcamp
---

Yet another article on SOLID. Why? Most articles focus on making these abstract principles more concrete. I'm going in the other direction. Hopefully hitting on things you could call ["first principles"](https://en.wikipedia.org/wiki/First_principle). This is **not** an introduction.

In this article I will use subjective, loosely-defined, abstract terminology. That's the point. I aim to be *very brief*. I hope you revisit this article as your definitions evolve and gather new insights. I'll try to update it as mine do too.

# First Abstraction

The first iteration takes the "known" definitions of the SOLID principles and produces short, analogous, higher-level statements.

## SRP – Single Responsibility Principle

> Your thing should do only **one** thing.

I can't think of many things at the same time. It's hard to use or change something that I don't understand.

## OCP – Open/Closed Principle

> It should be easy to do more, and hard to do less.

Suddenly doing less, breaks the contract I have with others. Inevitably people want me to do more, it would be nice if that were easy.

## LSP – Liskov Substitution Principle

> A special type of thing, is still a thing.

If you say you can do one thing, but also do other things. Those other things shouldn't interfere with you fulfilling your first duty.

## ISP – Interface Segregation Principle

> The less I know about you, the better.

There might be many aspects to you. But give me a finger, and I *might* take your whole hand.

## DIP – Dependency Inversion Principle

> I don't depend on you, I depend on something **like** you.

I don't want the police officer's home phone number, I want to call 911 and get help!

# Second Abstraction

The second iteration aggregates and abstracts the ideas some more.

## SRP + ISP + DIP

> I can do more with less

## LSP + ISP + DIP

> A deal is a deal! Read the contract!

## SRP + OCP + LSP + ISP + DIP

> I want to be free to change.

and/or

> I'm selfish. You're a black box to me.

# Third Abstraction

Even more abstract...

> Specify, but keep it short.

and

> Build on top of things that don't change.

# Finally...

After four iterations, my efforts produce this "first principle".

> Connect the pieces using only a few, well-defined, and lasting support structures.

# Final thoughts

Perhaps it was inevitable that my "first principle" ended up the way it did. [My research on modularity](/2017/09/03/Modularity-part1.html#research) brought me to the same conclusion, and I have been looking at the world through those glasses ever since. This idea is ubiquitous. You can see it in [Rich Hickey's "Simple Made Easy" talk](https://www.youtube.com/watch?v=rI8tNMsozo0&feature=youtu.be&t=6m4s). Where he puts it as:

> "Architectural agility dominates!"

Software design principles are often contradictory. There is tension between wanting "fewer components" *and* "smaller components". There are no truths, only trade-offs. This distilled principle is no different. Different interpretations of it will lead to contradictions. What it has going for itself is that it is, itself, a **single** principle.
