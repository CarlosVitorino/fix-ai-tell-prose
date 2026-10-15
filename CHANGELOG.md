# Changelog

## 0.3.0 (unreleased)

- Apply copy fixes directly to local page or component source by default; the owner
  reviews the diff afterward. Markdown issues reports and approval gates are opt-in.
- Return edited text for pasted copy and validate source edits with project checks.
- Keep unresolved factual questions out of page copy and raise them in the final response.
- Preserve protected wording and require explicit authorization for commits, pushes,
  deployment or live-CMS changes.
- Align supporting guidance and add a direct-edit contract regression test.

## 0.2.0 (unreleased)

- Replace the mandatory 13-pattern review procedure with editor-led writing principles
  and voice guidance. Findings no longer require a numbered pattern or cluster.
- Accept exact project source and rendered interface copy; extraction helpers are optional.
- Keep factual fidelity, protected wording, untrusted-content handling and owner approval.
- Add a simple review example and remove sentence-length quotas from the SaaS preset.
- Retain the old pattern catalogue and tally format as optional compatibility references.
- Make the main skill's pattern summary optional in structural validation.

## 0.1.0 (unreleased)

- First batch of 13 patterns (AT-01 to AT-13) with detection criteria, false-positive
  guidance, fix rules, replacement tables and examples.
- Two-pass review workflow with fact, voice and new-tell audit.
- Review file format with per-finding decisions; site index for URL lists.
- `pages.py`: URL list and sitemap expansion; prose extraction to numbered blocks, with
  network, size and XML safety limits.
- `tally.py`: per-pattern approval rates from reviewer decisions.
- Rulebook validator, regression cases, unit tests and CI.
