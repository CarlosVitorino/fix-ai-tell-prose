# fix AI-tell prose

An agent skill for reviewing website copy that reads as AI-written and proposing plain,
human fixes, which a person approves before anything changes on the site.

Site owners and agencies hire a developer to go through their pages. The developer loads
this skill into Claude Code (or any agent that reads the Skills format), points it at the
client's URL list or sitemap, and gets one review file per page. Each flagged passage comes
with the named pattern, why it reads as AI-written, and a concrete before→after rewrite.
The reviewer marks each fix approved, edited or rejected.

It is **not** a detector: it gives no AI-likelihood scores. And it **never publishes**:
the output is a review, not a diff.

## Status

Version 0.1.0, first batch of 13 patterns. Built and unit-tested; **not yet validated on
real pages with a human reviewer** (see `docs/validation-log.md`). That validation is the
next step, and the rest of the plan depends on its result.

## Quick start

```bash
make install-skill          # links the skill into ~/.claude/skills/
```

Then, in Claude Code:

> Use fix-ai-tell-prose to review https://client.example/about

or, for a whole site:

> Use fix-ai-tell-prose to review the pages in urls.txt for client.example and write the
> reviews to reviews/client-example/.

After the reviewer has marked decisions:

```bash
python3 skills/fix-ai-tell-prose/scripts/tally.py reviews/client-example/
```

## What is in the box

```
skills/fix-ai-tell-prose/
  SKILL.md                      workflow, guardrails, pattern summary
  references/patterns.md        AT-01..AT-13: detection, false positives, fix, before→after table
  references/voice-calibration.md
  references/review-format.md   review file and site index format, with a worked example
  references/page-pass.md       working down a URL list or sitemap
  scripts/pages.py              URL list/sitemap expansion; page → numbered prose blocks
  scripts/tally.py              per-pattern approval rates from reviewer decisions
evals/cases.json                regression cases, including false-positive checks
tools/validate_skill.py         structural check of the rulebook (used by CI)
docs/                           build plan, runbook, validation protocol and log, roadmap
```

The first batch:

| ID | Pattern |
| --- | --- |
| AT-01 | Chatbot leftovers and knowledge-cutoff disclaimers |
| AT-02 | Throat-clearing openers and signposting |
| AT-03 | Stock AI vocabulary |
| AT-04 | Wordy filler constructions |
| AT-05 | Stacked hedges |
| AT-06 | Avoiding "is" and "has" |
| AT-07 | Inflated significance and legacy |
| AT-08 | Brochure language |
| AT-09 | ", highlighting..." tails |
| AT-10 | "Not just X, it's Y" contrasts |
| AT-11 | Reflexive triads |
| AT-12 | Vague attribution |
| AT-13 | Generic upbeat conclusions |

## Development

```bash
make install-dev   # pytest and ruff (development only; the skill itself has no dependencies)
make check         # lint, tests, rulebook validator — the same as CI
```

Changing a pattern: edit `references/patterns.md`, keep the SKILL.md summary table in step,
add or update a case in `evals/cases.json`, run `make check`. Never renumber pattern IDs.

## Documents

- `build-brief.md`: the original brief.
- `docs/build-plan.md`: phases, assumptions and decisions.
- `docs/runbook.md`: running a client engagement, and troubleshooting.
- `docs/validation-protocol.md`: how to test the rulebook with a real reviewer.
- `docs/validation-log.md`: results (none yet).
- `docs/pattern-roadmap.md`: candidates for later batches.
- `SECURITY.md`: threats and mitigations.

## Credits and license

The pattern catalogue draws on Wikipedia's WikiProject AI Cleanup guide "Signs of AI
writing" and on [blader/humanizer](https://github.com/blader/humanizer) (MIT), with the
two-pass structure inspired by
[NulightJens/humanizer-stack](https://github.com/NulightJens/humanizer-stack). All
descriptions, tables and examples here are original writing.

MIT licensed; see `LICENSE`.
