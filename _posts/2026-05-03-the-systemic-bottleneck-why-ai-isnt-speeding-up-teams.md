---
title: "The Systemic Bottleneck: Why AI Isn't Speeding Up Teams"
date: 2026-05-03
tags: [ai, software, productivity, teams]
published: true
---

## The Individual Illusion

As teams adopt AI for coding, we are seeing that AI doesn't *necessarily* provide a team-level productivity boost, even though individuals experience one. [Research from Uplevel (2024)](https://resources.uplevelteam.com/gen-ai-for-coding) analyzed thousands of developers and found that while individuals *felt* faster, there was **no significant increase in team-level cycle time or throughput**, and it even noted a potential increase in "burnout-related" metrics because the systemic bottlenecks remained. This discussion has been frequent recently, and it is becoming clear: writing code was **never actually the bottleneck**.

<picture>
  <source
    type="image/webp"
    srcset="/images/IMG_9191-640.webp 640w, /images/IMG_9191-960.webp 960w, /images/IMG_9191-1280.webp 1280w, /images/IMG_9191.png 1408w"
    sizes="(max-width: 768px) calc(100vw - 3rem), 672px">
  <img
    src="/images/IMG_9191-960.png"
    srcset="/images/IMG_9191-640.png 640w, /images/IMG_9191-960.png 960w, /images/IMG_9191-1280.png 1280w, /images/IMG_9191.png 1408w"
    sizes="(max-width: 768px) calc(100vw - 3rem), 672px"
    width="1408"
    height="768"
    alt="siloed teams connected by tangled, frail bridges representing broken working agreements"
    loading="lazy"
    decoding="async">
</picture>

## The Forgotten Warning

While AI coding is undeniably making things faster, it isn't doing so in a **systemic** way. This brings us back to Fred Brooks and his timely article, ["No Silver Bullet."](https://worrydream.com/refs/Brooks_1986_-_No_Silver_Bullet.pdf) Brooks did a fantastic job of distilling a message that many people feel intuitively. Referring to that article and going back to read it is a great way to organize the thoughts you have as a person working in software development. It provides a solid foundation and a thought structure to organize the concepts in your brain.

## The Local Optimization Trap

AI acts as a local optimization by speeding up the "accidental" parts of the job—the actual writing of the code. However, what is left behind **now dominates our overall speed**. We are still facing the irreducible complexity of the analysis problem: figuring out what the user *actually* wants and iterating on those ideas. Any productivity boost in coding is simply drowned out because we haven't solved the **essential complexity** of the work.

## The Role of Modularity

This is where the core concept of modularity applies. It provides a unique perspective on human dynamics in organizations and team structures. The same concept of having stable interfaces between code components also applies to the **contracts** between specialties within a team. We should look at the working agreements between a developer and a UX designer, a Product Owner, or the support desk.

## The Flexibility Paradox

This flexibility in human communication is a **double-edged sword**. In software, the changing of the code structure over time makes it glaringly obvious when we've made the wrong abstraction. However, because humans are able to figure things out and find ways to solve problems, there isn't a strong incentive to design an efficient and stable system. Our own flexibility **makes the flaws less obvious**, allowing us to tolerate systems that don't actually work well. But we tolerate this at a cost. The resulting frustration and job dissatisfaction are things we cannot ignore. We are able to fix the problems, but we aren't **happy** about it.

## Friction as Waste

The real friction isn't the fact that we communicate, but that we **have** to communicate because information is missing. In an ideal world, you would have all the information to execute a work package without needing more. In reality, we hardly ever get a ticket that is complete. This leads to handovers that cause change failures—failures in quality that **force you to go back** and ask questions. The [GitClear "Coding on Copilot" report](https://www.gitclear.com/coding_on_copilot_data_shows_ais_downward_pressure_on_code_quality) illustrates this perfectly: while code was being written faster, **quality was declining**, leading to more "churn" (code that is rewritten or deleted shortly after being pushed), which means the rework drowns out the speed.

Our current processes, like Scrum ceremonies, tend to be ineffective at solving this. They are *necessary*, but we need more structure than just getting together for a daily meeting. Generally, people go into meetings unprepared and don't know what their contribution should be. This often results in plenary meetings where everyone discusses tickets that aren't relevant to them.

(Before my ex-colleagues crucify me: yes, I know the theory says it *is* relevant because we are "one team" on "one product," but I'm commenting on what I have seen **in practice**, not what the theory says. In reality, most developers aren't happy in these meetings, and the PO isn't happy about the lack of participation. For whatever reason, they **just don't work**.)

We should ask what a process would look like where we wouldn't **need** these meetings. There are other ways to tackle this, such as asynchronous communication or grouping people into smaller sub-teams, but the way ceremonies are generally done is not effective.

## The Working Agreement as API

Looking at these interfaces is a good way to measure our effectiveness as a group. Our working agreements should be the **stable interfaces** that drive us toward high performance. We have to ask how often we have to work **despite** our working agreements instead of in accordance with them.

## The Systemic Conclusion

We should not treat people like code, as formalizing everything is a bad idea. However, we must ensure our agreements are things we work **with**, not things we work **around**. To truly gain from AI, we must fix the interfaces that allow our individual gains to be swallowed by systemic friction.
