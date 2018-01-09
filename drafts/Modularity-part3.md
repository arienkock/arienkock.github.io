---
title: "Modularity Deep Dive - pt. 2"
teaser: modules and your process
---

[Part 1](/2017/09/03/Modularity-part1.html) | Part 2

# Modules and Methodology
The better a module boundary is defined, the fewer modules are affected by changes to your system. This lets different people work on parts of the system at the same time, while being isolated from each other. 

Adding new members to a team does not make them faster or more effective, *unless* they can collaborate well enough to compensate for the increased overhead. 

Modules that are drawn up ahead of time (the best time), are defined with incomplete information. When you notice a trend of cross-cutting concerns, then it's time to redraw the boxes. But what do you do when there is a team who's responsible for a module? What if that module no longer exists after the refactor?

A company can increase the number of developers, but somewhere there is an inflection point. The more thoughtful and deliberate you are about defining responsibilities (for both people and code) the further you can push the size of your team. Get too attached to an instance of those boundaries, then you've missed the point. The separation of concerns is to enable change. How the separation happened may turn out to be wrong, and you have to be able to change that.

Modularity is working when it allows parallel development. When that stops being the case, it's time to have a chat. It's easy to recognize those moments of friction inside an organization. Because, you start sensing this misalignment. You notice a conflict of interests, when you should all be working towards the same goal. Someone might misbehave and now it's personal. My team, my poduct, my service... pride gets attached to the wrong thing and now there's *actual* conflict. Good luck fixing that.

Places where this happens often:

1. where front end meets back end
1. where dev meets ops
1. where visual design meets front end
1. where marketing meets dev
1. where budgeting and planning meet implementation

It shouldn't come as a surprise that developers have a developer-centric view of the world. It's a question of empathy, that determines how we interact with someone outside of our tribe. It's especially obvious when we depend on someone that doesn't need anything from us. Operations needs to keep servers up. Devs need to push changes, and for that they need ops. What does ops need dev for? Unless you align the values, there will be friction. 

Organizational modularity is about defining contracts. We can negotiate contracts, but they must be able to change. When we notice too many cross-cutting changes in code, we redraw the boxes and the lines. When we notice too much micro-management, too much push-back from ops, too many ad-hoc features from marketing, we generally don't take a step back to change things. And by we I mean people in general. A corporate environment is hierarchical, but relatively static across time. If we discover a deficiency, reorganizing is seen as this epic change imposed from the top down. Meanwhile, people on the front-lines may want different changes. Clearly it would be benifitial if organizational changes were easy. And we'd only ever think of making them easy if they were the norm, and not the exception. This is a lesson from Extreme Programming. Making small incremental changes to *how people work together* lets us react quickly to friction and conflict. In other words, it gives us *organizational agility*.

