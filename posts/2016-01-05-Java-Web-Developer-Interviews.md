---
title: Java Web Developer Interviews
teaser: No more coding tests
---


I've tried conducting interviews with developers in different ways, and I've learned a few things from these experiences:

1. People tend to have enough interviews going on around the same time that an hour and a half long coding test is more of an annoyance than a welcome challenge.
2. Coding tests don't kickstart a technical assesment any more than words do.
3. Coding tests usually don't showcase the candidate's intent.
4. Day to day challenges require "Googling it", which coding challenges purposely _try_ to avoid.

## No more coding tests?
In the latest interview I conducted, I decided to do a pair programming exercise. It's more of a "talk me through your process while solving a fictional issue"-exercise. This was much more effective in showcasing this candidate's experience, proficiency with his/her preferred IDE, and basic Java language knowledge.

## How is it any different?
You might say: "..but that's still a coding test". I suppose that's true, but it's still very different. The best part is that I could see and talk to the person doing the test, which told me a lot more than only the end-product could.

The candidate struggled with something. So what? That's not the end of the exercise. I help out of course, because the exercise was about to challenge them in a new and different aspect of a developer's tasks. I couldn't have given them this problem and walked away, because they would have spent a lot time overcoming an obstacle that had nothing to do with the task. Different skills combine to make a good developer, but traditional (blind-review) coding tests seem to dumb it down into two or three dimensions.

## The ideal task
The ideal task will cover the most common or important aspects of the developer's job. This is different for each organization, but for me I wanted to emphasize:

1. Ability to navigate code using their preferred tools.
2. Interpreting and internalizing an unfamiliar project structure.
3. Tendency to re-use vs creating new functionality.
4. Considering edge-cases and performance.

Our exercise was:

> "When I submit this form I can update entity X. I want the first letter of each word of this entity's field Y to be converted to upper-case when I do so."

Can the candidate figure out where in the code-base the save action is performed? Once found, what are their considerations when deciding where to add the functionality? Do they think to check if the entity is modified anywhere else?

At a high level, do they understand what the components should do? Do they have any useful feedback about naming, dependencies and project structure?

Do they consider looking online for a utility that capitalizes words or do they dive straight into writing a for-loop? Do they know what you're talking about when you discuss `StringTokenizer` vs `String.split()`?

When asked to implement their own version of the capitalizer functionality, and perhaps given some hints about Unicode, are they aware of the consequences of treating everything like ASCII?

String concatenation in a for-loop cannot be optimized into `StringBuffer` appends by the compiler, does the candidate know this? Do they know why it matters?

During such an exercise the candidate will most likely feel a lot of pressure to perform. I tried to lighten this, but I think most interviewers will invariably fail. People get nervous, and you can't completely avoid this without drugs. However, it's not a bad thing to see how they deal with this. Above almost every technical aspect and despite what some code-whisperers may say, during a pair programming exercise you will see much more of the person's personality than you would through their code alone.
