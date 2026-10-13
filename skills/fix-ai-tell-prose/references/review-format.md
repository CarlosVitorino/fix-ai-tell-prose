# Review file format

One Markdown file per page. A person reads it, decides on each finding, and the developer
applies only what was approved. `scripts/tally.py` parses this format, so keep the
headings and field labels exactly as shown.

## Rules

- File name: the URL path in kebab case, e.g. `services-roof-repair.md`; `home.md` for
  the root. For pasted copy, a short name the person chooses.
- The **Before** text is quoted exactly as extracted, including its punctuation. Never
  tidy it.
- The **After** text is the full replacement for the quoted passage, ready to paste, or
  `(delete)`.
- Each finding heading is `### F<n> · <pattern ID> <pattern name> · <block ID>`, with
  findings numbered from 1 in page order.
- `Decision:` is always written as `pending`. Allowed values for the reviewer: `pending`,
  `approved`, `edited`, `rejected`.
- `Protected:` is `yes` when the passage is legal text, a quotation, a testimonial, a
  price or spec, or an owner-protected term (see SKILL.md Non-negotiables 5).
- `Also:` lists other pattern IDs that hit the same passage, or is omitted.
- No scores, percentages or verdicts about authorship anywhere in the file.

## Template

````markdown
# Prose review: <page title>

| Field | Value |
| --- | --- |
| URL | <url, or "pasted copy"> |
| Retrieved | <YYYY-MM-DD> |
| Source | <"pages.py extract" / "HTML file from owner" / "pasted"> |
| Words reviewed | <number> |
| Rulebook | fix-ai-tell-prose <version>, patterns AT-01 to AT-13 |
| Findings | <total> (<ID> ×<count>, ...) |

**Status:** awaiting review. Nothing on this page has been changed.

**Voice note:** <five-line voice note from voice-calibration.md, or "defaults (no sample)">

**Scope notes:** <out-of-scope blocks, protected terms, assumptions; or "none">

## Findings

### F1 · AT-09 ", highlighting..." tails · b004

**Before**

> <exact passage>

**After**

> <replacement, or (delete)>

**Why it reads as AI-written:** <one or two sentences tied to the pattern's criteria>

**Check before approving:** <facts the reviewer must confirm, owner questions; or "nothing">

Also: <other pattern IDs; omit this line if none>
Protected: no
Decision: pending
Reviewer note:

## Outside this batch

<tells noticed that are not in AT-01 to AT-13, without fixes; or "none">
````

## Worked example

This example uses invented copy for an invented business, to show the format. It is not
validation evidence.

````markdown
# Prose review: About Us — Northgate Plumbing

| Field | Value |
| --- | --- |
| URL | https://northgate-plumbing.example/about |
| Retrieved | 2026-10-13 |
| Source | pages.py extract |
| Words reviewed | 214 |
| Rulebook | fix-ai-tell-prose 0.1.0, patterns AT-01 to AT-13 |
| Findings | 3 (AT-02 ×1, AT-07 ×1, AT-09 ×1) |

**Status:** awaiting review. Nothing on this page has been changed.

**Voice note:** "We" and "you"; contractions yes; short sentences; trade register ("job",
"call-out"); prices in £. Source: owner's emailed newsletter, March issue.

**Scope notes:** Gas Safe registration text (b011) is protected and not reviewed.

## Findings

### F1 · AT-02 Throat-clearing openers and signposting · b002

**Before**

> In today's fast-paced world, finding a plumber you can trust has never been more
> important.

**After**

> (delete)

**Why it reads as AI-written:** A general scene-setting opener that says nothing about
Northgate; the next sentence is where the page starts.

**Check before approving:** nothing

Protected: no
Decision: pending
Reviewer note:

### F2 · AT-07 Inflated significance and legacy · b003

**Before**

> Since 2009, Northgate Plumbing has played a pivotal role in keeping Sheffield homes
> running, and our growth stands as a testament to our unwavering commitment to quality.

**After**

> We've fixed boilers, leaks and blocked drains in Sheffield since 2009.

**Why it reads as AI-written:** "Pivotal role" and "testament to our unwavering
commitment" claim importance without a fact behind them. The only facts are the year and
the city; the services come from b006.

**Check before approving:** the service list matches what you want to lead with.

Also: AT-03
Protected: no
Decision: pending
Reviewer note:

### F3 · AT-09 ", highlighting..." tails · b007

**Before**

> Every engineer carries a fully stocked van, ensuring a seamless experience for our
> customers.

**After**

> Every engineer carries a fully stocked van, so most jobs are finished on the first
> visit.

**Why it reads as AI-written:** The ", ensuring a seamless experience" tail comments on
the fact instead of adding one.

**Check before approving:** "most jobs are finished on the first visit" comes from b008;
if you'd rather not repeat it, cut the tail instead.

Protected: no
Decision: pending
Reviewer note:

## Outside this batch

Em dashes in four of nine paragraphs (not in this batch; noted only).
````

## Site index

For a URL list, keep `reviews/<site>/index.md`:

````markdown
# Prose review index: <site>

Rulebook: fix-ai-tell-prose <version> · Started: <date> · Pages listed: <n>

| # | URL | Review file | Findings | Status |
| --- | --- | --- | --- | --- |
| 1 | https://client.example/ | home.md | 5 | reviewed |
| 2 | https://client.example/about | about.md | 3 | reviewed |
| 3 | https://client.example/pricing | — | — | fetch failed: HTTP 403 |
| 4 | https://client.example/terms | — | — | skipped: legal page (out of scope) |
| 5 | https://client.example/team | team.md | 0 | reviewed: no findings |
````

Status values: `reviewed`, `reviewed: no findings`, `fetch failed: <reason>`,
`skipped: <reason>`, `not started`. Every listed URL gets a row, so nothing silently
drops out.
