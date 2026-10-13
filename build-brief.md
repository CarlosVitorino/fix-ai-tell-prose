# fix AI-tell prose
## What this is

Site owners and agencies pay a developer to crawl their sitemap, score each page for AI-sounding prose, and present human-approved fixes rather than auto-publish them.

## What would make you stop

nothing!

## The smallest thing worth building first

One SKILL.md (plus a small references/ folder) covering a first batch of the highest-confidence AI-tell patterns, each with detection criteria and a before→after replacement table, tested by running it against a handful of real pages and confirming a human reviewer would approve the rewrites. If it produces fixes you would actually sign off on, the crawl-and-score service wrapper can follow.

## What this is not building

- An automated detector or linter-first tool — the rulebook prescribes fixes, it does not score first
- Auto-publishing fixes to live sites — everything is human-approved before it lands
- A hosted crawler or sitemap-scanning service in the first version
- A web UI or dashboard — the interface is the agent loading the skill
- Exhaustive coverage of all 29 patterns before the first ones are validated
- A proprietary license — the reference projects are MIT and the format is the proven convention

## What good output looks like

Each flagged passage comes with the named pattern, why it reads as AI-tell, and a concrete before→after replacement — the humanizer model compresses wordy constructions to their plain equivalents ("in order to achieve this goal" becomes "to achieve this"), collapses stacked hedges, and pairs every tell with the fix. Output is a review artifact for a human to approve, not a diff that gets merged on its own.

## What it reads from

A SKILL.md plus a references/ folder in the Claude Code Skills convention — the format three of the four best projects in this space already ship, so agents handle it natively. The core rulebook is sourced from Wikipedia's WikiProject AI Cleanup "Signs of AI writing" guide; blader/humanizer is the model to match: ~4,500 words, 29 numbered patterns with detection criteria and replacement tables, voice calibration, and a two-pass audit. A page-by-page pass should support working down a sitemap list of URLs supplied by the site owner or agency.

## What it must never do

It must not auto-publish anything — the whole premise is human-approved fixes presented back to the owner or agency. It is not a detector or a score, so it should not present numeric AI-likelihood ratings as the product; it names the problem and prescribes the fix.

## Who it is for

Site owners and agencies who pay a developer to crawl their sitemap, score each page for AI-sounding prose, and present human-approved fixes. The skill is the engine a developer carries into that engagement; per the material's own framing, nothing about this would make them stop.

## Existing work to build on

blader/humanizer (github.com/blader/humanizer) is the single best model: one ~4,500-word SKILL.md, 29 numbered patterns, MIT licensed, 16k stars. NulightJens/humanizer-stack contributes a two-pass pipeline separating surface tells from deeper rewrites. The Claude Skills directory (e.g. aicodedecode-humanizer, graded A) and the ai-content-humanizer GitHub topic map the rest of the field and the shipping convention.

## Evidence

- [ai-content-humanizer · GitHub Topics · GitHub](https://github.com/topics/ai-content-humanizer)
- [Humanizer Skill: The Complete Guide to blader/humanizer for Claude Code](https://agentpedia.codes/blog/humanizer-claude-code-skill-guide)
- [Blader Humanizer in 2026: What v3.1 Changed and How I Use It - DEV Community](https://dev.to/farahellison/blader-humanizer-in-2026-what-v31-changed-and-how-i-use-it-5h6b)
- [GitHub - NulightJens/humanizer-stack: Two-pass pipeline for removing AI writing tells from outward-facing text: a surfa…](https://github.com/NulightJens/humanizer-stack)
- [Humanizer (Grade A) - Claude Skill | Skills Directory](https://www.skillsdirectory.com/skills/aicodedecode-humanizer)
