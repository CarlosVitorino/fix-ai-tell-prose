# Build plan — fix AI-tell prose

Size: **Full product**. A production-ready product: sound architecture, tests, security, monitoring and documentation, built in reviewed stages.

A starting plan in five phases. Tick them off as you go, rewrite them freely, and put your own decisions at the bottom.

## 1. Plan
- [ ] Restate the idea and who it is for in your own words, and list what you are assuming.
- [ ] Choose the stack and note why. Ask the person if two choices are close.
- [ ] Rewrite phases 2 to 5 below for this project.
- Done when: the person has read the plan and agreed.

## 2. Foundation
- [ ] Considered architecture, CI and environments from the first commit.
- Done when: the project runs locally with one command.

## 3. Core
- [ ] Every feature in the brief, with proper accounts, permissions and, where needed, payments.
- [ ] Target: One SKILL.md (plus a small references/ folder) covering a first batch of the highest-confidence AI-tell patterns, each with detection criteria and a before→after replacement table, tested by running it against a handful of real pages and confirming a human reviewer would approve the rewrites. If it produces fixes you would actually sign off on, the crawl-and-score service wrapper can follow.
- Done when: the smallest thing worth building first works.

## 4. Harden
- [ ] Broad tests, security review, performance, accessibility and error monitoring.
- Done when: the person is comfortable putting it in front of someone.

## 5. Ship and learn
- [ ] Staged rollout, backups, runbooks and analytics tied to the stop condition.
- [ ] Measure: nothing!
- Done when: there is evidence for or against the idea.

## Decisions

_Record choices and the reasons for them here._