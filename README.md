# fix AI-tell prose

An agent skill for editing website copy directly into clearer, more human writing in
the owner's voice. The owner reviews the source diff after the agent makes the changes.

Site owners and agencies hire a developer to go through their pages. The developer loads
this skill into Claude Code (or any agent that reads the Skills format), points it at the
client's project files or pasted copy, and gets edited copy, validation results and a
short explanation of what changed. No separate Markdown issues report is required.

It is **not** a detector: it gives no AI-likelihood scores. Local editing does not
authorize commits, pushes, deployment or live-CMS changes.

## Status

Version 0.3.0: direct source editing by default, with writing principles, voice and
optional supporting references. The agent does the editorial work; neither numbered
patterns nor pending approval files are required. Report-only work is opt-in.

## Quick start

```bash
make install-skill          # links the skill into ~/.claude/skills/
```

Then, in Claude Code:

> Use fix-ai-tell-prose to fix the copy in this project's About page. Apply the edits
> directly; I will review the diff.

or, for a whole site:

> Use fix-ai-tell-prose to fix this project's public pages and interface copy.

The agent reads the source, applies focused copy changes and validates them. You review
the changes afterward. Unresolved factual questions stay out of the page and are reported
in the final response. If you supply only a URL, the agent needs access to editable source.
Ask explicitly for an audit without edits when you want a report instead.

## What is in the box

```
skills/fix-ai-tell-prose/
  SKILL.md                      editor-led instructions and guardrails
  references/writing-principles.md  meaning, specificity, voice and rhythm
  references/patterns.md        optional AT-01..AT-13 examples, not a gate
  references/voice-calibration.md
  references/voice-saas.md      voice preset for SaaS / AI-tool sites
  references/review-format.md   optional report-only format; not the default deliverable
  references/page-pass.md       optional legacy report-only URL-list workflow
  scripts/pages.py              optional extraction; omits forms and other interface text
  scripts/tally.py              optional tally for legacy numbered AT-pattern reviews only
evals/cases.json                legacy pattern examples; not automated agent evaluations
tools/validate_skill.py         file/reference checks (not editorial quality tests)
docs/                           project history and validation notes
```

The principles cover clear meaning, specific details, natural rhythm and consistent
terminology. The agent should also question unsupported generalizations, unclear metaphors
and repetition across the whole piece. Preserve useful character rather than making every
sentence short and every paragraph alike. The old pattern catalogue remains available
when examples help, but it no longer limits the review.

## Development

```bash
make install-dev   # pytest and ruff (development only; the skill itself has no dependencies)
make check         # lint, tests, rulebook validator — the same as CI
```

Change writing guidance in `references/writing-principles.md` and voice guidance in the
voice references. Keep the main skill small. Run `make check` for helper and packaging
regressions; it does not prove the quality of an agent's rewrites. Validate those by
reviewing real copy with the owner. Preserve legacy pattern IDs for existing reviews.

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
