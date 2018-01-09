---
title: "Modularity Deep Dive - pt. 2"
teaser: what does a module look like
---

[Part 1](/2017/09/03/Modularity-part1.html) | Part 2

A module, as a logical unit, can be implemented in any number of ways. Its *form* is simply "some code with a public interface". Which includes, but is not limited to:

1. classes
2. packages
3. web-services

That means we can discuss the modularity of a class, the package it's in, and the service it's part of. The concept of modularity isn't limited to any one of these levels. This article is about general guidelines for building modules, that apply to all of them.

When you google the word module you get this definition:

> module: each of a set of standardized parts or independent units that can be used to construct a more complex structure, such as an item of furniture or a building.

Notice the words "parts" and "construct". Modules are meant to be part of a bigger thing. You're *supposed* to build things with them. In short: a module has connecting bits. 

Next, take the word "standardized". Manufacturers solved the problem of modularity a long time ago. Replacing parts in cars, washing machines, or computers would be a whole lot harder if they hadn't. How do you standardize code? You define the "connecting bit" exactly, and do your best not to make breaking changes to it.

## Standardizing parts

An example at the level of a service would be the healthcheck endpoint. You could decide on a convention of putting the healthcheck endpoint at `/health` and letting it return a `200` code when it's healthy. That makes composing services with a load-balancer much easier. That's standardizing in a way that makes change (i.e. adding new services) easier. 

If your class implemented a `Lifecycle` interface, it could be placed in some container that manages it. The interface is the standardized connecting bit. The class implementing the interface depends only on this abstraction and is shielded from changes to the container's implementation, as long as this contract doesn't change.

At the level of functions, normally each one has its own signature. That's the opposite of standard. Imagine a codebase where all functions were standardized to take and return a single argument of a hash/map/dict type. Composing functions would be a breeze. You could also make a lot of changes without having to recompile dependant code, because your signatures never change. Granted, there are downsides to this, but it's the equivalent of standardized parts and it *would* make change easier. Which is why we do any of this in the first place.

## Building bigger things

Composing functions is a good way of thinking about software composition. The more standard the signature is, the easier composition becomes. All your utility functions become universal, because they can be applied to all other functions. If everything has the same shape, everything can interconnect effortlessly. Like Legos.

Even though details about modules will differ, the parts they have in common help us integrate them. For example, at the service level, messaging can be shared. Services can declaratively specify what topics they are interested in and which ones they intend to publish events on. If all services did this and message formats were standard, then a higher level process could easily wire them up together so they can communicate without knowing anything about how messages are actually serialized and routed. They could be in the same process for all they know, it wouldn't matter.

At each layer of your system, cross-cutting concerns can become part of the common shape of the modules. Things like logging, metrics, and communication are almost universal. They make good candidates for becoming part of that connective tissue.

Having common shapes is only helpful when you have multiple similar things. It doesn't make sense to build an archetype when there is only ONE implementation. However, it does help to at least think of your module that way. A good example is data storage. Even if you only have one implementation, it's benefitial to think about what your API would look like if you used a different database. This will help you identify places where your abstraction is leaking information.

## Conclusion

Modular design is applicable to almost any domain. Making standard parts is about API design, and the challenge is designing an API that hides the appropriate information. A great tool in API design is imagining what the API might look like if you reimplemented it. Because, who knows, one day you might want to.

[Part 1](/2017/09/03/Modularity-part1.html) | Part 2