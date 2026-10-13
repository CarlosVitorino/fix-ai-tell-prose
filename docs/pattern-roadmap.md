# Pattern roadmap

The brief points at a full catalogue of about 29 patterns (the size of blader/humanizer,
built on Wikipedia's "Signs of AI writing" guide) but says not to write all of them before
the first ones are validated. The first batch (AT-01 to AT-13) is in
`skills/fix-ai-tell-prose/references/patterns.md`. These are candidates for later batches,
in rough order. None has detection rules or fixes yet, on purpose.

| Candidate | Why it is not in the first batch |
| --- | --- |
| Em dashes as the default connector | Many human writers and house styles use them; needs a rate threshold calibrated on real pages |
| Bold on every phrase | Often a CMS or designer choice, not the writer's |
| Title Case In Every Heading | Common house style; low confidence on websites |
| Emoji as bullets or headings | Brand-dependent |
| Curly vs straight quotes mixed | Usually CMS or copy-paste, not a writing tell |
| One-line closers and dramatic fragments ("That's the real win.") | Strong tell, but needs care on landing pages where short punchy lines are a deliberate style |
| Sayings that sound deep ("At its core, ...") | Overlaps with AT-07; split out once data shows it is common |
| Repeated sentence openings | Needs whole-page view; good candidate for batch 2 |
| Hyphenated compound pile-ups ("data-driven, customer-centric, future-ready") | Overlaps with AT-03 and AT-11 |
| Elegant variation (rotating synonyms for the same thing) | Hard to fix without changing meaning |
| False ranges ("from X to Y" where X and Y are not ends of a scale) | Medium confidence |
| "Challenges and future prospects" section formula | Mostly in long articles, rare on business sites |
| Heading repeated in the first sentence | Partly covered by AT-02 |
| Re-explaining what the reader knows | Hard to judge without knowing the audience |
| Passive voice and missing subjects | High false-positive rate on technical pages |
| Sycophantic or over-warm tone toward the reader | Overlaps with AT-01 |

Add a candidate to a batch only with: detection criteria, false-positive guidance, a fix
rule, a replacement table of at least five rows, an example, at least one regression case
in `evals/cases.json`, and a reason from a validation run (it was missed, or reviewers
asked for it). `make check` enforces the structural parts.
