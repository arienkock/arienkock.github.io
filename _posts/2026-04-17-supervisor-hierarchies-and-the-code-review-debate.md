---
title: What supervisor hierarchies can teach us about code reviews in the AI era
subtitle: Reliability thinking from Erlang, applied to a messy engineering debate
date: 2026-04-17
tags: [engineering, ai, code-review]
published: false
---

One of Joe Armstrong's enduring ideas is that resilient systems are not built by pretending failure will not happen. They are built by assuming failure is normal, then shaping the system so failures are isolated, detected quickly, and recovered from automatically.

That mindset came through strongly in his talks about supervisor hierarchies: small processes doing one thing, linked into trees, with supervisors deciding what to restart and when. The point is not perfection in each worker process. The point is resilience in the whole.

I keep thinking about that while watching the current "what do we even do with code reviews now?" debate, especially with AI-assisted coding becoming normal.

## The framing problem

A lot of arguments about code review get stuck because they frame review as a gate for catching bad code before merge, full stop.

That was never the whole story, but AI makes the limitation obvious:

- Generated code can look plausible while hiding subtle design mistakes.
- Volume goes up, so reviewer attention becomes the scarcest resource.
- If we treat every PR as a full manual audit, we burn people out.

So the old binary framing breaks down:

- "Review everything deeply" does not scale.
- "Review nothing, just ship" fails predictably.

The more useful question is: what review structure gives us system-level resilience when individual changes and individual reviewers will both fail sometimes?

## Supervisor trees as a mental model for review

In supervisor hierarchies, responsibilities are explicit and layered. We can map that to code review practice.

### Layer 1: local checks (worker-level)

This is linting, tests, static analysis, type checks, policy checks, and AI-generated review hints. These are cheap, fast, and relentless.

They should catch routine breakage so humans do not spend cognition on obvious defects.

### Layer 2: peer review (first-line supervisor)

A human reviewer focuses on what automation is still bad at:

- domain fit
- architectural alignment
- maintainability
- clarity of intent

This is not "find every bug." It is "is this change healthy for the system?"

### Layer 3: ownership and architecture review (higher-level supervisor)

High-risk areas need stronger supervision: security-sensitive modules, core platform code, distributed system boundaries, money movement, privacy logic, data model migrations.

Not every PR needs this level. But some absolutely do, and pretending otherwise is just wishful thinking.

### Layer 4: production feedback loops (recovery strategy)

Even good review systems miss things. Resilience comes from what happens next:

- observability that spots regressions early
- feature flags and rollout controls
- quick rollback paths
- post-incident learning that feeds back into checks and review heuristics

This is the equivalent of restart strategy. If your only safety mechanism is "catch it in PR," your recovery model is weak.

## What this means for the AI code review debate

I think both extreme positions are wrong:

- "AI means human review is obsolete"
- "AI means every line now needs more human review than before"

AI changes where effort should go, not whether effort is needed.

The opportunity is to move humans up the stack:

- less time on syntax-level policing
- more time on system boundaries and risk
- clearer ownership for high-consequence changes

Put differently: AI can be an excellent worker process in the review hierarchy, but it should not be the entire supervision strategy.

## A practical policy I would start with

If I had to set team policy tomorrow, I would start with this:

1. **Default automation-first checks.** No human reviews for changes that fail baseline quality gates.
2. **Risk-tiered human review.** Lightweight review for low-risk changes, deeper required review for high-risk areas.
3. **Explicit ownership matrix.** Define who must review what, based on blast radius.
4. **Fast recovery discipline.** Every significant change needs rollback and monitoring plans.
5. **Monthly calibration.** Sample escaped defects and review misses; adjust rules instead of blaming individuals.

This is not glamorous, but it is robust.

## Where I still feel tension

There is still a cultural question here: teams often use review for mentorship, alignment, and social trust, not just defect prevention. If we over-automate, we might save time but lose learning.

I do not have a perfect answer yet. My current view is that we should separate goals instead of mixing them:

- keep mandatory review focused on risk and correctness
- create intentional spaces for mentoring and design discussion

When those are conflated, both get worse.

## Draft notes to expand

- Add one concrete example of a "looked fine in review, failed in production" change and show how layered supervision would have reduced impact.
- Reference one specific Joe Armstrong quote/talk segment for precision.
- Add a short section on incentives: velocity metrics often punish resilient review behavior.

That is where I am landing right now: code review should be designed like a resilient system, not a single checkpoint. Assume mistakes, structure recovery, and put scarce human judgment where it matters most.
