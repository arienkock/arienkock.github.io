---
title: What Agents Can Do For You
subtitle: For when you're done putting off learning this stuff
date: 2026-05-25
tags: [productivity, ai]
published: false
---

Are ytou not sure what an agent is and how it's different from an AI chat? Have you been meaning to give Claude Cowork or ChatGPT Codex a try, but still haven't?

This article's goal is to get you informed and excited enough to get you across that line, and start getting your hands dirty.

I _could_ start listing practical use cases or use metaphors like "2nd brain" and "personal assistant" to get you inspired. But instead I'm going to point you at thoughts you likely have during the day, and how your cognitive patterns could change for the better:  

- **Thought:** "I could, but I don't have time"

  **Becomes:** "I'll make a prototype"
  
- **Thought:** "I don't know"

  **Becomes:** "Let me skill up real quick"

- **Thought:** "I'm overwhelmed"

  **Becomes:** "Let me analyze my task list for priority and quick win progression"

**Disclaimer:** It's very easy to read any productivity tips/hacks as an insinuation that you simply need to work harder or smarter. It's a stressful to think that you're being wasteful, or lagging behind the times. I get that feeling too. Don't let it that feeling take over. Take note of the information, and judge yourself by your intentions and your effort. Let's not compare ourselves to hypothetical others, or an idealised version of ourselves.

With that out of the way...

# What is an Agent
These days, that means something like:

> An **LLM** used from an **agent harness** that gives it access to **tools** and runs it in a **loop** until the user's current goal is reached.

Breaking that down:

LLM == A large language model. It could run on your own computer, but usually it runs on a powerful GPU-based server somewhere in a datacenter. You call it via a regular web API.

Agent Harness (a.k.a. Scafflod) == a desktop, mobile, or web application that sits between the user and the LLM providing both with some additional features that make it look like the LLM can "act" and help the user organise their work.

Tools == LLMs that were trained to use tools can, in their message responses, indicate their "intention" to use a tool. The Agent Harnass picks up on that message and executes that tool (often asking for user permission first). Tools range from fetching a web page, to executing code on your machine. What makes this funky is that sometimes when an agent harnass calls its "brain"/LLM it isn't a plain LLM on the other end, but in fact another agent which has its own tools available. So agents can be composed in this sense.

Loop == Before agents became the default way to interact with LLMs, the chat was a single request followed by a single response. Now a request can lead to many subsequent responses where the LLM is having a conversation with itself and the agent harness. At some point the LLM indicates it is done, and a final response is generated for the user. Using this loop-until-finished approach, agents can potentially resolve very complex problems and tasks with minimal interaction.

# Everything Is Becoming an Agent

When you use Claude, ChatGPT, or Gemini via the web-api you're talking to an agent, not a bare LLM. Why? Because it has tools, and it takes multiple steps before providing a final answer. You still have interfaces where this is not the case, but it's hard to draw the line exactly when something becomes an agent. Is simply having tools enough to be labeled as one? A more useful question for our purposes is: "What do I want from my agent?"
