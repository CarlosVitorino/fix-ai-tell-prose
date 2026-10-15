# Runbook: editing copy

The default is direct local source edits, followed by owner review of the diff.
Report-only work must be explicitly requested. Do not commit or publish automatically.

## Before the engagement

1. Install the skill: `make install-skill` (links it into `~/.claude/skills/`), or copy
   `skills/fix-ai-tell-prose/` into the project's `.claude/skills/` folder. Any agent that
   reads the Skills format (SKILL.md plus references/) can load it.
2. If using the optional helpers, check Python 3.10+ is available. The skill itself does
   not require an extraction script or a particular tool.
3. Agree with the client, in writing:
   - which copy (project files, pasted text, pages or a URL list, plus any exclusions);
   - protected terms: brand phrases, SEO keywords, product names;
    - which editable source files own the copy;
    - that fixes are applied locally for the owner to review afterward, without deployment;
    - who reviews the diff (the owner, their editor, or the agency).
4. Ask for a writing sample in the owner's own voice (see
   `references/voice-calibration.md`).

## During the engagement

1. Load the skill and read the whole piece. Identify the owning source and existing user
   edits. If source edits automatically publish, use an isolated checkout or ask first.
2. Choose how to read the exact source. The optional `pages.py urls` helper can expand a
   sitemap, but source files, pasted copy and rendered pages are valid too. Check interface
   copy omitted by extraction, such as form text and dialogs, separately.
3. Apply the smallest effective copy changes directly. Preserve markup, expressions,
   protected wording and behaviour; leave unsupported claims for owner clarification.
4. Check facts and voice, inspect the diff, run project checks and check text fit in the
   rendered interface when available. Do not write owner-question placeholders into pages.
5. Summarize changed files, validation, coverage limits and unresolved questions in chat.
   Do not create Markdown issue files or pending decisions unless explicitly requested.

## After the owner reviews

1. Revise the edited copy in response to owner feedback. Do not revert unrelated user work.
2. Commit or publish only when explicitly requested, using the project's normal process.
3. For an explicit report-only engagement, the optional `references/review-format.md`
   example and legacy `tally.py` helper remain available. They are not prerequisites for
   direct editing; the tally only understands numbered AT-pattern reports.

## When things go wrong

| Symptom | Cause | What to do |
| --- | --- | --- |
| `pages.py: error: HTTP 403 from ...` | Site blocks unknown user agents or bots | Ask the client to allow-list the review or send saved HTML; run `extract` on the file |
| `refusing ...: it resolves to a non-public address` | URL points at a private or local host | Correct the URL; for a staging copy on your own network use `--allow-private` |
| `only N words extracted` warning | Page is rendered by JavaScript, or has little prose | Ask for saved HTML from a browser ("Save page as") or the CMS export |
| `refusing redirect from ... to ...` | Redirect to a non-http(s) or private target | Use the final public URL directly |
| `sitemap declares a DOCTYPE or entities` | Unusual or hostile sitemap | Ask for a plain URL list |
| `child sitemap limit (20) reached` | Very large sitemap index | Use `--include` to scope, or pass the child sitemaps one at a time |
| Agent quotes text that is not in the source | Quote was paraphrased or taken from a different version | Discard the quote; verify the exact source passage using files, HTML or a rendered page |
| Same copy appears on several pages | Repeated site-wide block | Edit its shared source once, or update the in-scope copies consistently |
| `tally.py: warning: ... has decision 'maybe'` | Reviewer used a value outside the four allowed | Ask them to pick approved, edited, rejected or pending |

## Monitoring

There is no server to monitor. For direct editing, report the checks run, failures and
coverage limits in the final response. Optional helper failures remain visible:

- each helper prints one `error:` line on stderr and exits non-zero;
- report-only site indexes can record every URL's status, including fetch failures;
- `tally.py --strict` checks missing decisions in legacy reports, not source-edit quality.
