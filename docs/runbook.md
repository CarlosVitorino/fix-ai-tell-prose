# Runbook: running a review engagement

For the developer an owner or agency hires to review their pages.

## Before the engagement

1. Install the skill: `make install-skill` (links it into `~/.claude/skills/`), or copy
   `skills/fix-ai-tell-prose/` into the project's `.claude/skills/` folder. Any agent that
   reads the Skills format (SKILL.md plus references/) can load it.
2. Check Python 3.10+ is available (`python3 --version`). The helpers need nothing else.
3. Agree with the client, in writing:
   - which pages (a URL list or sitemap, plus any exclusions);
   - protected terms: brand phrases, SEO keywords, product names;
   - that the deliverable is review files, and nothing is changed on the site until they
     approve each fix;
   - who reviews (the owner, their editor, or the agency).
4. Ask for a writing sample in the owner's own voice (see
   `references/voice-calibration.md`).

## During the engagement

1. Start a fresh agent session in an empty working folder (not the client's site repo, so
   nothing can be written into their content by accident).
2. `python3 ~/.claude/skills/fix-ai-tell-prose/scripts/pages.py urls <sitemap> > urls.txt`
   and confirm the count and scope with the client.
3. Ask the agent to review the pages with the skill, writing to `reviews/<site>/`.
4. Spot-check three review files yourself before sending anything: facts unchanged,
   protected text marked, voice right, no scores.
5. Send the review files (or a zip of `reviews/<site>/`) to the reviewer.

## After the reviewer decides

1. Run `tally.py reviews/<site>/` and keep the table with the engagement notes.
2. Apply only findings marked `approved` or `edited` (using the reviewer's edited text),
   through the client's normal publishing process. Applying is a separate, explicit step;
   the skill never does it on its own.
3. Feed rejections back into the rulebook: open an issue or PR with the rejected finding
   and the reviewer's note.

## When things go wrong

| Symptom | Cause | What to do |
| --- | --- | --- |
| `pages.py: error: HTTP 403 from ...` | Site blocks unknown user agents or bots | Ask the client to allow-list the review or send saved HTML; run `extract` on the file |
| `refusing ...: it resolves to a non-public address` | URL points at a private or local host | Correct the URL; for a staging copy on your own network use `--allow-private` |
| `only N words extracted` warning | Page is rendered by JavaScript, or has little prose | Ask for saved HTML from a browser ("Save page as") or the CMS export |
| `refusing redirect from ... to ...` | Redirect to a non-http(s) or private target | Use the final public URL directly |
| `sitemap declares a DOCTYPE or entities` | Unusual or hostile sitemap | Ask for a plain URL list |
| `child sitemap limit (20) reached` | Very large sitemap index | Use `--include` to scope, or pass the child sitemaps one at a time |
| Agent quotes text that is not on the page | Agent used a summarising web tool instead of `pages.py` | Discard that review; re-run the page with `pages.py extract` output |
| Same fix proposed on every page | Repeated site-wide block | Follow "Repeated blocks" in `references/page-pass.md` |
| `tally.py: warning: ... has decision 'maybe'` | Reviewer used a value outside the four allowed | Ask them to pick approved, edited, rejected or pending |

## Monitoring

There is no server to monitor. Failures are visible in three places, by design:

- each helper prints one `error:` line on stderr and exits non-zero;
- the site index records every URL's status, including `fetch failed: <reason>`, so no
  page silently drops out;
- `tally.py --strict` exits non-zero if any decision is missing or unreadable, so a
  half-reviewed batch cannot be mistaken for a finished one.
