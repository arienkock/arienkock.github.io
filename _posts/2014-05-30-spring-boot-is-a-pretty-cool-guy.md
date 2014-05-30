---
layout: post
---
Forgive the use of an ancient internet meme, but things like [Spring Boot](http://projects.spring.io/spring-boot/) make me very excited. Whether [eh afraids of anything](http://knowyourmeme.com/memes/pretty-cool-guy) or not, it does allow you to get up and running with Spring MVC + Spring Security really fast.

###It's a bird... it's an app... it's a webapp###
You can run a Java SE application from command line and get all the Spring framework support you want, but I am (as probably most other people are) interested in making web-applications. IMHO the most elegant thing about Spring Boot is being able create a WAR deployable in the traditional manner that is also an executable JAR at the same time. I've created an app like this for one of my clients, and because I was responsible for deploying it and configuring the VPS this saved me a lot of time and effort.

A tip here is that if you setup your Upstart scripts to restart the service on failure is to make sure the location the WAR is unpacked to (happens each time) is cleaned up regularly. 

###The defaults###
With `@EnableAutoConfiguration` Spring Boot will inspect your classpath during startup and load things like an embedded database. The HSQLDB `Datasource` will be available to wire into any beans you define, or if you add Hibernate to your classpath you won't even need to do THAT. To kickstart this process even more, you can add a starter project as a Maven dependency, which in turn includes the things you need in a more concise manner without creating a huge POM. Think of it as a buffet. Pick some Spring Data MongoDB for persistence, a little bit of Thymeleaf for templating, etc. The complete list is available [here](https://github.com/spring-projects/spring-boot/tree/master/spring-boot-starters).

The more you care about your configuration (like the location of your HSQLDB file) the more work you need to do. It's like I said in my post on Spring Roo, if you use it for what it's good at, it's smooth sailing through and through. I may not have said that exactly, but I meant to. You can start writing a class that is your Configuration class with `@Bean` annotated methods, as well as your Controller with your `@RequestMapping`s. A single file application! Who **DOESN'T** want that? Am I right? Ok, so no reasonably sized application would do that, but you don't **always** make big webapps.

###Bottom line###
Like a framework, Spring Boot does more than you need. It will never be a slim fit. Customizing Spring Boot behavior is easy, so your experience with Spring Boot will be very similar to having a template starter project of your own that you can clone each time and adapt to your needs. Even though Spring Boot now has made the creation of such a template project extremely easy with the added benefit of flexible deployment.

I would like to point out that I am not a fan of Spring MVC's startup times. Spring Boot does add a bit to that and so it isn't as fast as I'd like it to be. In the future I'd like to see stripped down version of Spring Framework that does nothing by default, forcing you to think about what you want and what you need instead of remembering to turn off the things you don't.