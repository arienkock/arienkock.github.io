---
published: false
layout: post
---


To organize code I've started to adopt certain tools and methods. [Dependency inversion](https://en.wikipedia.org/wiki/Dependency_inversion_principle) is the principle that is fundamental in achieving this, and [interfaces](/2015/06/25/the-point-of-interfaces.html) are the primary tool (or language feature, if you prefer) Java devs use to achieve dependency inversion. But wait, there's more...

### Maven `runtime` scope
When you split your project into modules, you're trying to seperate concerns. You're trying to make sure that each module has clear responsibilities. At some point the implementations of your abstractions have to interact. Your actual top-level application depends on all your modules, either directly or transitively. Normally, using only your abstraction modules (maven modules containing *only* interfaces) that would create a very large number of modules: one for each layer, one for each abstraction between layers, +1 for the final top level layer of your application. This is where the `runtime` scope can help. Using this you can depend on code that you're not allowed to use directly. If you do, `mvn compile` will fail. However, all the dependencies are included in your artifacts, so using a dependency-injection framework you can load all the implementations at runtime while still decoupling your components at build-time.

