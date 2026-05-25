---
title: The Best Use of AI In Your Development Cycle
subtitle: What supervisor hierarchies can teach us about code reviews in the AI era
date: 2026-05-25
tags: [engineering, ai, code-review]
published: true
---

I suspect that most people pushing for AI adoption in organisations are doing it with the intent of writing better code faster. One would expect to see a boost in developer productivity. And you do, kind of, but only at the level of the individual. As I claimed in a previous article: ["Writing code is rarely the bottleneck"](https://arienkock.github.io/2026/05/14/if-not-coding-then-what/).

[DORA's recent AI ROI report](https://cloud.google.com/resources/content/dora-roi-of-ai-assisted-software-development) shows a dip in quality/stability during early AI adoption. So what we're saying then is that AI adoption, the way it's usually done, does not boost overall productivity. It puts such a high load on the quality gates that we actually produce lower quality changes.

I suspect most people's reactions when finding this out is either "The data must be wrong!", "I told you so!" or... "I've been scammed!".

## The Verification Gap / Crisis

When AI-written code is usually good enough, you start checking it less. When AI-written code is written in such high volume that you can't keep up, you start checking it less.

People have written about how verifying/checking code is becoming a bigger part of our work. And that's not something people are generally excited about. The prompting part is fun, but the checking part is not. It takes quite a bit of time and energy. Check out:

- [When AI Writes the World's Software, Who Verifies It? - 
Leonardo de Moura](https://leodemoura.github.io/blog/2026-2-28-when-ai-writes-the-worlds-software-who-verifies-it/)
- [The Verification Crisis: Why Checking Generated Code Is Harder Than Writing It](https://smarterarticles.co.uk/the-verification-crisis-why-checking-generated-code-is-harder-than-writing-it)

This isn't new, because this was the sucky part of code reviews to begin with. And now we have to do it more often? No thanks.

## A Hierarchy of Verification

Erlang popularised the concept of supervision hierarchies. The core idea is that you can get highly fault-tolerant systems if you build them in such a way.

If our goal is defect tolerance instead of fault tolerance, then a hierarchy of verification should be a powerful architecture. It simultaneously addresses the bottleneck of reviews, while enabling us to broaden the scope of verifications via automation. Automation handles menial and repetitive verifications better than humans do.

Take this example: have AI check for conceptual duplication, i.e. code that may look different, but mean the same thing. You're going to get what you asked for, but some of them might not be feasible to fix. Other are just the AI making stretch. Have adversarial reviews, an AI can check that work and reduce the noise. If you're going to ask for a code review from an AI, you're always going to get **something**. Have that work checked in a hierarchy of verifications, and it could actually end up concluding that it's good to go.

The human sits at the top, because (of course) the human developer takes final responsibility for the result. It's a human checking the work of an AI that checked a human's work.

With the rise of token costs this may sound like yet another way to burn through cash. But there are definitely ways to deal with that.

## AI Verification On a Budget

Having an LLM read the entire codebase for every update is expensive. Nobody is questioning that. Token costs will skyrocket with continuous manual AI checks.

However, many verification checks can be evaluated deterministically. If a verification can be performed by looking at an AST or directory structure, there may already be a tool there to do it. If so, use AI to write the rule. If not, use AI to write the check as code.

That's leverage. Having AI write code that replaces itself completely, or in part, is how you truly scale up the benefits. Also, if the AI bubble goes bust, you still have your custom-built tooling.

Some checks are partially deterministic and partially subjective. Have AI write a script to wrap the AI in a harness. These scripts isolate the problem and only call the LLM for the subjective bits.

## You Can Start Right Now

Who is the person that you wish would review every PR? Ask them to imagine what they would review if they had infinite time and motivation. What are the invariants? What are the architecture rules that live in their mind and materialised through past decisions?

Use this documented wishlist as your foundation for automated rules. Have your team use AI to generate deterministic tests for these rules. Implement these generated tests directly into your continuous integration pipeline.

Identify the remaining complex rules from the wishlist. Frame them as full agent prompts with structured outputs that your CI pipeline can pick up.

## Conclusion: Targeted Improvements to Your Software Delivery Performance

Automating verifications addresses the most likely bottlenecks: human verifications. Addressing your system's constraint gets you higher throughput. In particular, this approach also gets you (in all likelihood) higher quality changes. It doesn't have to break the bank if you're smart about it.

There is only one reason I can think of that this isn't the first and most common use of AI in software development. Reviewing and maintenance are some of the least fun things to do for a developer.

Well great! If it hurts, do it more often. Make it easier, cheaper, and faster. What's stopping you?
