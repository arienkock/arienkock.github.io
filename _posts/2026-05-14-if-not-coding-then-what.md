---
title: "The Moving Target: Why AI Coding Tools Haven't Fixed Your Bottleneck"
date: 2026-05-08
tags: [ai, software, developers, productivity]
published: true
---

In my previous article, I claimed that the bottleneck in software delivery is rarely actually the coding itself. This explains why most companies aren't seeing a organization-wide increase in productivity despite the new wave of AI tools. _(See [Research from Uplevel (2024)](https://resources.uplevelteam.com/gen-ai-for-coding) and [DORA: ROI of AI-assisted Software Development report](https://cloud.google.com/resources/content/dora-roi-of-ai-assisted-software-development))_

That begs the question: if it’s not the coding, **what is the bottleneck?**

In my personal experience, the answer is neither constant nor universal. It’s rarely one single thing at all times. Instead, I believe there is a set of likely culprits that compete day to day for the honor of "delivery bottleneck". It is a story about [efficiency of flow, stability, and quality](https://dora.dev/guides/dora-metrics/). If that sounds like I'm looking at it as a value-stream, then you're right on the money.

Here are the primary bottlenecks as I see them.

## 1. The Erosion of Core Work

The biggest limitation on an organization's throughput is the sheer amount of time spent on things that aren't software delivery. I use developers as the obvious example, but this applies to every role.

As I see them, a developer's core responsibilities at a high level are:

* **Refinement:** Understanding what needs to be built and why. This includes technical designs and and non-functionals like security. AI can help here, but I don't see it applied often.
* **Execution:** Building the thing and reviewing the work of peers. This is the part that most people target with AI coding agents.
* **Maintenance:** Keeping the code clean, refactoring, and updating dependencies to maintain long-term velocity. AI coding tools can definitely help here too. But in general this never gets enough attention. Even before AI, so that hasn't changed.
* **Operational Health:** Monitoring performance and seeing how things behave in production.

However, these responsibilities are **constantly under pressure** from (mostly) necessary distractions like HR tasks, performance evaluations, endless meetings with stakeholders, and sudden escalations. Then there are the new ad-hoc initiatives (often handed down from higher management) that don't fall into the team's core work. I’m not saying we should do away with these things entirely, but we have to admit they put **a massive squeeze on the time actually spent delivering software**. 

## 2. The Fan In and the Integration Trap

Another major bottleneck is **the integration of multiple parallel changes**. We often see teams working on separate tracks, which eventually results in large batches of code being merged at once for various reasons.

There is often a time squeeze and fan in right before a release acts as a massive throughput blocker. It makes it much harder to push to production regularly, regardless of how fast the individual features were coded.

This may sound like this is an engineering problem. In part it is, since we can always choose to do fewer things at a time and do more together. However, this is **also a consequence of feature scoping and slicing** (or lack thereof).

## 3. The Review/QA Handoff

In between the coding and the integration, there is the simple hurdle of getting code reviewed and tested by a fresh pair of eyes. *Segregation of Duties* is an important quality and security guideline. But it is a **[handoff](https://dora.dev/capabilities/loosely-coupled-teams/#:~:text=Number%20of%20handoffs%3A%20Count%20the%20number%20of%20handoffs%20a%20typical%20feature%20or%20change%20requires%20to%20get%20from%20%22code%20complete%22%20to%20%22released%20to%20users.%22) by definition**. This creates a stop-and-start rhythm that kills momentum.

## From Bad to Worse

When your teams are struggling things tend to get worse not better. When you have a large blast radius, you naturally encounter more issues that are harder to troubleshoot. Disappointing delivery performance can lead to well-meaning interventions by management that risk making things worse:

 - **More teams working in parallel** - Leads to more integrations pressure, more meetings, more responsilibity dead-zones.
 - **Grow the team** - Almost guaranteed short term performance dip. Increased stress on existing team. It's a gamble. A bad hire sucks the energy out of everyone.
 - **Extract QA/Security/Ops into a separate team** - The goal is to gain focus time, but unless you manage to make those teams be practically invisible to one another (smooth handoffs and no meetings or coordination needed) you're not going to get it. It's a typical local optimization.

Exactly the same intervention, **but executed well** *can* lead to performance gains. But my point here is that it's actually really hard to do these org changes well. So we should postpone them until we're highly confident they'll work.

Keeping things small and in close proximity (a small single multi-disciplinary team) allows us to compensate for bad process. That may sound cynical, but it's more an acknowledgement that making an optimal process that _both teams and their stakeholders are eager to adopt_ is... hard.

## Damn, That's Bleak Bro..

I started off talking about AI coding and then went down the value-stream Lean detour around mis-management mountain. But now we're back and the question is _"what do we do about it?"_ and _"can AI help?"_.

To do anything about this you need knowledge of theory and of people. Have a focused dialog with an LLM, and it is likely to help you organise your thoughts.

But what theory? There's so much work out there that all references and builds on top of one another, and it's hard to point at one thing. So here is a (mostly) unordered and incomplete list:

- [Continuous Delivery](https://continuousdelivery.com/)
- [Accelerate](https://itrevolution.com/product/accelerate/)
- [The Goal](https://northriverpress.com/the-goal-a-process-of-ongoing-improvement/) and [Theory of Constraints](https://www.tocinstitute.org/theory-of-constraints.html)
- [All the state of DevOps reports and research on the DORA website.](https://dora.dev/publications/)
- [Lean Software Development](https://www.oreilly.com/library/view/lean-software-development/0321150783/)
- [The Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)
- [Process control diagrams](https://en.wikipedia.org/wiki/Control_chart)


Then how do you apply that knowledge to identify your constraints and come up with an initiative? How do you propose it in such a way to maximise your chances of people giving it a good-faith attempt?

## Start the Conversation

Here's a prompt you can paste directly into any AI chat. Tweak the options below to match your situation, then copy it.

<style>
.pb{border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.5rem;background:var(--card);margin:2rem 0}
.pb-group{margin-bottom:1rem}
.pb-group>span{display:block;font-size:.75rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--muted-foreground);margin-bottom:.5rem}
.pb-opts{display:flex;flex-wrap:wrap;gap:.4rem}
.pb-opt{padding:.3rem .85rem;border:1px solid var(--border);border-radius:999px;background:transparent;color:var(--foreground);font-size:.875rem;font-family:var(--font-sans);cursor:pointer;transition:all 150ms ease-out;line-height:1.4}
.pb-opt:hover{border-color:var(--primary);color:var(--primary)}
.pb-opt.on{background:var(--primary);border-color:var(--primary);color:#fff}
.pb-out{margin-top:1.25rem}
.pb-pre{background:var(--muted);border:1px solid var(--border);border-radius:var(--radius);padding:1rem;font-family:var(--font-sans);font-size:.875rem;line-height:1.65;white-space:pre-wrap;word-break:break-word;color:var(--foreground)}
.pb-row{display:flex;justify-content:flex-end;margin-top:.75rem}
.pb-btn{padding:.45rem 1.25rem;background:var(--primary);color:#fff;border:none;border-radius:var(--radius);font-family:var(--font-sans);font-size:.875rem;font-weight:600;cursor:pointer;transition:background 150ms ease-out}
.pb-btn:hover{background:var(--primary-hover, #0f766e)}
.pb-btn.ok{background:#16a34a}
</style>

<div class="pb">
  <div class="pb-group">
    <span>Your role</span>
    <div class="pb-opts" data-g="role">
      <button class="pb-opt on" data-v="I'm a software developer on the team.">Developer</button>
      <button class="pb-opt" data-v="I'm a team lead or engineering manager.">Team Lead / EM</button>
      <button class="pb-opt" data-v="I'm a director, VP of Engineering, or CTO.">Director / VP / CTO</button>
    </div>
  </div>
  <div class="pb-group">
    <span>Primary symptom</span>
    <div class="pb-opts" data-g="symptom">
      <button class="pb-opt on" data-v="Our biggest pain is that things take too long to ship.">Too slow to ship</button>
      <button class="pb-opt" data-v="Our biggest pain is that too many bugs reach production.">Too many bugs</button>
      <button class="pb-opt" data-v="Our biggest pain is that we are constantly firefighting and reacting to incidents.">Always firefighting</button>
      <button class="pb-opt" data-v="Our biggest pain is that delivery timelines are unpredictable.">Unpredictable timelines</button>
    </div>
  </div>
  <div class="pb-group">
    <span>Session goal</span>
    <div class="pb-opts" data-g="goal">
      <button class="pb-opt on" data-v="Help me identify what the main bottleneck is.">Find the bottleneck</button>
      <button class="pb-opt" data-v="I have a hunch about the bottleneck — help me validate or challenge it.">Validate my hunch</button>
      <button class="pb-opt" data-v="Once we identify the bottleneck, help me build a concrete action plan.">Get an action plan</button>
    </div>
  </div>
  <div class="pb-out">
    <div class="pb-pre" id="pb-text"></div>
    <div class="pb-row">
      <button class="pb-btn" id="pb-copy">Copy prompt</button>
    </div>
  </div>
</div>

<script>
(function(){
  var TMPL="Help me understand the bottleneck in my software delivery process. Use everything you know about DORA research, Continuous Delivery, Accelerate, Lean Software Development, Theory of Constraints, The Goal, The Mythical Man-Month, and statistical process control.\n\nInterview me using the Socratic method. Ask focused questions, one at a time. Keep your responses under 100 words. Aim to pinpoint the bottleneck in fewer than 20 questions.\n\nContext: {role} {symptom} {goal}";
  var s={role:"I'm a software developer on the team.",symptom:"Our biggest pain is that things take too long to ship.",goal:"Help me identify what the main bottleneck is."};
  function render(){document.getElementById("pb-text").textContent=TMPL.replace("{role}",s.role).replace("{symptom}",s.symptom).replace("{goal}",s.goal);}
  document.querySelectorAll(".pb-opts").forEach(function(g){
    g.querySelectorAll(".pb-opt").forEach(function(b){
      b.addEventListener("click",function(){
        g.querySelectorAll(".pb-opt").forEach(function(x){x.classList.remove("on");});
        b.classList.add("on");
        s[g.dataset.g]=b.dataset.v;
        render();
      });
    });
  });
  var btn=document.getElementById("pb-copy");
  btn.addEventListener("click",function(){
    navigator.clipboard.writeText(document.getElementById("pb-text").textContent).then(function(){
      btn.textContent="Copied!";btn.classList.add("ok");
      setTimeout(function(){btn.textContent="Copy prompt";btn.classList.remove("ok");},2000);
    });
  });
  render();
})();
</script>