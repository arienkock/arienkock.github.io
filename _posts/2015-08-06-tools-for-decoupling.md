---
published: true
layout: post
---


To organize code I've started to adopt certain tools and methods. [Dependency inversion](https://en.wikipedia.org/wiki/Dependency_inversion_principle) is the principle that is fundamental in achieving this, and [interfaces](/2015/06/25/the-point-of-interfaces.html) are the primary tool (or language feature, if you prefer) Java devs use to achieve dependency inversion. But wait, there's more...

### Maven `runtime` Scope
I like this one, but I don't think it's very common. When you split your project into modules, you're trying to seperate concerns. You're trying to make sure that each module has clear responsibilities. At some point the implementations of your abstractions have to interact. Your actual top-level application depends on all your modules, either directly or transitively. Normally, using only your abstraction modules (maven modules containing *only* interfaces) that would create a very large number of modules: one for each layer, one for each abstraction between layers, +1 for the final top level layer of your application. This is where the `runtime` scope can help. Using this you can depend on code that you're not allowed to use directly. If you do, `mvn compile` will fail. However, all the dependencies are included in your artifacts, so using a dependency-injection framework you can load all the implementations at runtime while still decoupling your components at build-time.

### Application Containers
There's Spring, OSGi and to a lesser extent DI-only tools like Dagger and Guice. They implement some form of inversion-of-control. An application can be composed declaratively. Instead of saying "Use component A", your code now says "I require something that looks/behaves like component A". Where "component A" could be an abstraction/interface. This declarative style let's you hook into a larger process, one that is aware of or can discover components _for_ you. It's basically a plug-in mechanism... or service discovery... which means...

### Microservices
As much as the microservice hype is overblown, it _is_ (like it or not) a good way to decouple. What it's missing is the plug&play nature of something like DI. If all your applica... err.. I mean... **microservices**... were to magically wire themselves up, wouldn't that be great? Is there something like that? If there is, I don't know about it. Right now you still have to do most of the legwork yourself with tools like [Zookeeper](https://zookeeper.apache.org/) or [etcd](https://coreos.com/etcd/). Orchestration of application modules is something that is rapidly moving from the  multi-library, to the multi-process, and up to the multi-machine scale. Though I think in most cases we can do without this upscaling (most applications are not Twitter), it seems to be the trend. What is missing from that trend, is the awareness that it is the same age-old problem.

### Good people
The challenge of modularizing your code is one of knowledge and discipline. Knowledge of your subject matter and the business it's meant to service, and discipline to throw away previous assumptions and work (read: code) when new knowledge shines light on past mistakes. So, whether you write all your code into a single library, or write multiple distinct applications: ensuring your present and future productivity takes smart and hard-working people. i.e. the team is everything.
