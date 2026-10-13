# Build plan — fix AI-tell prose

Size: **Full product**, applied to what this product actually is: an agent skill plus a few
small local helper scripts, not a hosted app. Tick phases off as they land; decisions are at
the bottom.

## 1. Plan

- [x] Restate the idea and who it is for, and list assumptions (below).
- [x] Choose the stack and note why (see Decisions).
- [x] Rewrite phases 2 to 5 for this project.
- Done when: the person has read the plan and agreed. *(They asked for the whole build in one
  go and will review after, so phases were not paused for sign-off.)*

**The idea in my own words.** A developer is hired by a site owner or agency to go through
their pages and fix prose that reads as machine-written. The developer's tool is an agent
(Claude Code or any agent that reads the Skills format) loaded with this skill. For each page
the agent produces a review file: each flagged passage, the named pattern, why it reads as
AI-written, and a concrete rewrite. A person approves, edits or rejects each fix. Nothing is
published by the skill, and nothing is scored.

**Assumptions.**

1. "Score each page" in the brief means *triage by named findings*, not a numeric
   AI-likelihood rating, because the brief also says the product must never present one.
   The review lists how many findings of each pattern a page has; it gives no percentage,
   grade or probability.
2. The developer can run Python 3.10+ locally. The helper scripts use only the standard
   library, so there is nothing to install for the skill itself.
3. URLs come from the client (a list or a sitemap file/URL). The skill does not discover
   pages on its own.
4. English-language pages first. The patterns are written for English.
5. "Proper accounts, permissions and payments" from the generic plan template do not apply:
   there is no server, no users and nothing to charge for inside the skill. Billing happens
   in the developer's engagement, outside the product.

## 2. Foundation

- [x] Repository layout in the Skills convention (`skills/fix-ai-tell-prose/SKILL.md`,
      `references/`, `scripts/`).
- [x] MIT license.
- [x] One-command check: `make check` (ruff lint, unit tests, skill validator).
- [x] CI on GitHub Actions running the same command on Python 3.10 and 3.13.
- Done when: `make check` passes locally and in CI.

## 3. Core

- [x] `SKILL.md`: workflow, two-pass audit, guardrails, output contract.
- [x] First batch of 13 high-confidence patterns (`references/patterns.md`), each with
      detection criteria, false-positive guidance, a fix rule and a before→after table.
- [x] Voice calibration (`references/voice-calibration.md`).
- [x] Review file format with a per-finding decision field (`references/review-format.md`).
- [x] Page-by-page pass over a client URL list or sitemap (`references/page-pass.md`,
      `scripts/pages.py`).
- [ ] **Run against a handful of real pages and have a human reviewer approve the rewrites.**
      Blocked in the build environment (its network policy denies general web hosts) and the
      approval step needs a person in any case. The protocol is ready in
      `docs/validation-protocol.md`; results go in `docs/validation-log.md`.
- Done when: the validation run shows reviewers sign off on the fixes.

## 4. Harden

- [x] Unit tests for every script, including fetch limits and hostile input.
- [x] Structural validator for the rulebook so pattern edits cannot silently break the format.
- [x] Regression cases for the rulebook (`evals/cases.json`), including false-positive cases.
- [x] Security notes (`SECURITY.md`): untrusted page text, private-network fetch blocking,
      XML entity rejection, size and time limits.
- [x] Error reporting: scripts fail with one clear line on stderr and a non-zero exit code;
      the run index records per-page failures instead of dropping them.
- [x] Accessibility of the output: review files are plain Markdown with header rows on every
      table and no meaning carried by colour or emoji.
- Done when: the person is comfortable putting it in front of a client.

## 5. Ship and learn

- [x] Runbook for an engagement (`docs/runbook.md`).
- [x] Measurement tied to the real question ("would a reviewer sign off?"):
      `scripts/tally.py` turns reviewer decisions into per-pattern approval rates.
- [ ] Tag `v0.1.0` after the first validation run.
- [ ] Decide, from the tally, which patterns stay, which get rewritten, and whether to
      add the next batch or build the crawl-and-score wrapper.
- Done when: there is evidence for or against the idea.

## Decisions

- **Skill format, not an app.** The brief names the Skills convention and says the interface
  is the agent loading the skill. No web UI, no service.
- **Python standard library for helpers.** Every developer machine has Python; no
  dependencies means nothing to audit or pin for the shipped skill. `pytest` and `ruff` are
  development-only.
- **Helpers fetch and extract, they do not judge.** `pages.py` turns a URL into numbered
  text blocks so the agent can quote passages verbatim (web-fetch tools in agents often
  summarise, which breaks exact before→after quotes). No script looks for patterns; all
  detection is done by the agent reading the rulebook, as the brief requires.
- **Sitemap expansion is local and bounded.** `pages.py urls` reads a list or sitemap the
  client supplies (following at most 20 child sitemaps). It never follows links found in
  pages. This keeps it a helper, not a crawler.
- **First batch is 13 patterns, not 29.** Chosen for high confidence on website copy and
  for fixes that rarely change meaning. Formatting tells (dashes, bold, title case, emoji,
  curly quotes) are deferred because CMS templates and brand style guides produce them on
  purpose; see `docs/pattern-roadmap.md`.
- **Stable pattern IDs (`AT-01`…).** Review files and the tally key on them, so IDs are
  never renumbered; retired patterns keep their number.
- **Stop condition.** The brief's stop condition is "nothing!", which cannot be measured.
  Proposed instead, in `docs/validation-protocol.md`: if fewer than 60% of decided findings
  are approved (with or without light edits) across the first validation run, stop and fix
  the rulebook before building anything else.
- **Original wording.** The rulebook draws on Wikipedia's "Signs of AI writing" (CC BY-SA)
  and blader/humanizer (MIT) as sources of *which* patterns exist, but every description,
  table row and example here is written fresh, so the repository stays cleanly MIT.
