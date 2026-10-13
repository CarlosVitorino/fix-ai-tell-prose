# Validation protocol

The brief's first milestone is: run the skill against a handful of real pages and confirm a
human reviewer would approve the rewrites. This is how to do that and how to read the
result. It has **not been run yet**; results go in `validation-log.md`.

## What is being tested

Not "does the skill find AI writing" but "would a reviewer sign off on the fixes it
proposes". A finding the reviewer rejects costs them time and trust, so false positives
and meaning-changing rewrites count against the rulebook.

## Setup

1. **Pages.** 5 to 10 real pages from one to three sites whose owners agree to the review
   (your own sites, a friendly client, or an agency partner). Mix page types: at least one
   home or service page, one About page, one blog post. Include at least one page you
   believe a person wrote without AI help, as a false-positive check.
2. **Reviewer.** Someone who did not write the rulebook: ideally the site owner or an
   editor at the agency. They see only the review files.
3. **Agent.** Claude Code (or another Skills-compatible agent) with this skill installed
   (`make install-skill`), in a fresh session.

## Run

1. Put the URLs in `urls.txt`. Ask the agent: "Use fix-ai-tell-prose to review the pages
   in urls.txt for <site>. Write the reviews to reviews/<site>/."
2. Check the run index: every URL has a row; failures have reasons.
3. Give the reviewer the review files. For each finding they set `Decision:` to
   `approved` (would publish as is), `edited` (right call, they changed the wording) or
   `rejected` (wrong call, or the rewrite is worse), and add a note when rejecting.
4. Also ask the reviewer one question per page, recorded in the log: "Did the review miss
   anything that obviously reads as AI-written?" This catches false negatives.
5. Run `python3 skills/fix-ai-tell-prose/scripts/tally.py reviews/` and paste the table
   into `validation-log.md` with the reviewer's notes on rejections.

Also run the regression cases in `evals/cases.json` (paste each case's text, compare with
`expect` and `must_keep`) and record pass or fail per case.

## Reading the result

| Measure | Pass | Stop and fix the rulebook |
| --- | --- | --- |
| Accepted (approved + edited) of decided findings, all patterns | 80% or more | below 60% |
| Findings whose rewrite changed or added a fact | 0 | any |
| Findings on the human-written control page | 0 to 1 | 3 or more |
| Protected text rewritten without `Protected: yes` | 0 | any |
| Regression cases passing | all | any false-positive case failing |

Between 60% and 80%: tighten the detection criteria of the patterns `tally.py` marks
"tighten" or "revise or retire", re-run on the same pages, and compare.

Per pattern, `tally.py` needs at least 5 decided findings before giving a verdict. A
pattern that never fires on real pages after 10 pages is a candidate to move out of the
first batch.

## Proposed stop condition

The brief's stop condition is "nothing!", which cannot be checked. This protocol proposes:
**if the first validation run accepts fewer than 60% of decided findings, or any rewrite
changes a fact, stop and fix the rulebook before building the next batch of patterns or
the crawl-and-score wrapper.** If the owner of this project prefers a different threshold,
change it here and in `tally.py` (`KEEP_AT`, `STOP_BELOW`).
