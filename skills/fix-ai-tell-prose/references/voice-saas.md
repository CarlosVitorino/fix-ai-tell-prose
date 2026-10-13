# Voice preset: SaaS and AI software

Use this preset for software, SaaS and AI-tool sites when the owner gives no writing sample.
A sample from the owner always wins over this preset.

**Where it comes from.** It is modelled on the house style shared by the most respected
software product sites (the Stripe, Linear, Vercel, Notion, Figma and Anthropic school of
copy), described from general knowledge of their conventions, not copied from their pages.
What they share: the product is the subject, verbs say what it does, claims are specific
and checkable, and there is very little hype. A lot of AI-tool marketing does the opposite
("supercharge", "unlock", "revolutionize"), which is exactly what this skill removes.

## Voice note (paste into reviews)

```
Voice: SaaS preset (no owner sample). Product or "we" as subject; reader is "you".
Sentences: short and declarative, 6–14 words; one longer sentence per paragraph at most.
Contractions: yes, sparingly ("you'll", "it's"); none in legal or security copy.
Register: confident and precise, technical when the reader is technical; no hype, no
  exclamation marks, no emoji.
House rules: sentence-case headings; numbers as digits with units; name integrations,
  limits and prices exactly as the product does.
Source: references/voice-saas.md preset.
```

## The rules in practice

1. **Lead with what the product does, in a verb.** "Sync issues from GitHub in real time",
   not "Experience a seamless development workflow".
2. **One claim per sentence, and make it checkable.** A number, a named integration, a
   time, a limit, a price. If the page has no such fact, say less rather than inflate.
3. **Headlines are short statements, not slogans.** Five to eight words, sentence case,
   no colon-and-subtitle pattern, no question headlines.
4. **Say what the AI does, not that it is AI.** "Drafts a reply from the ticket history" beats
   "AI-powered support". Mention the model or method only if the page already does.
5. **Precise verbs over power verbs.** use, build, ship, send, sync, cut, find, draft,
   review, deploy. Not supercharge, unlock, unleash, revolutionize, transform, elevate,
   empower, reimagine.
6. **Talk to one reader.** "You" and the job they are doing. Not "teams of all sizes", not
   "whether you're a startup or an enterprise".
7. **Proof sits next to the claim.** A customer name, a metric or a link in the same block,
   or no claim. Never "trusted by leading companies" without the names.
8. **Calm endings.** A section ends on its last fact or on a plain call to action ("Start
   free", "Read the docs", "Talk to sales"), never on an upbeat summary.

## Before → after in this voice

| Before | After |
| --- | --- |
| Supercharge your workflow with our AI-powered platform. | Draft, review and ship docs from one editor. *(use the page's actual features)* |
| Unlock the full potential of your data with cutting-edge AI. | Ask questions about your data in plain English and get a chart back. *(if the page says so)* |
| Our revolutionary solution seamlessly integrates with your existing tools. | Connects to Slack, GitHub and Jira in a few clicks. *(only the integrations the page lists)* |
| Trusted by leading companies worldwide. | Used by [owner: customer names the page can show]. |
| Whether you're a startup or an enterprise, we've got you covered. | Free for up to 3 users. Paid plans from $12 per user per month. *(using the pricing page)* |
| It's not just a tool, it's your AI teammate. | It reads the ticket history and drafts a reply for you to edit. |
| Enterprise-grade security you can trust. | SOC 2 Type II, SSO and audit logs on every paid plan. *(only certifications the page states)* |
| The future of work is here. | (delete) |

## Watch out for

- **Don't make it terse to the point of vague.** "Fast. Simple. Powerful." is a triad of
  slogans (AT-11), not this voice.
- **Don't invent specifics to fit the style.** If the page has no numbers, the rewrite has
  no numbers; use an `[owner: ...]` question where a specific is clearly needed.
- **Security, compliance and pricing text is protected.** Flag, don't rewrite (SKILL.md,
  Non-negotiables 5).
- **Developer docs** follow the same voice but stay fully neutral: no "you'll love", no
  marketing claims, imperative mood for steps ("Run", "Set", "Deploy").
