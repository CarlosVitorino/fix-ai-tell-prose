# Patterns: first batch (AT-01 to AT-13)

Each pattern has the same parts:

- **Pass and threshold.** Which pass finds it, and whether one sighting is enough or it
  needs a cluster.
- **Detect when.** The criteria. Flag only when they are met.
- **Not a tell when.** The common false positives. Check these before flagging.
- **Fix.** The rule for the rewrite.
- **Replacement table.** Typical before→after pairs. They are starting points: always
  rewrite the actual sentence, never paste a row in blindly.
- **Example.** A short passage and its approved-style rewrite.

IDs are permanent. A retired pattern keeps its number and is marked retired; new patterns
get the next free number.

Why these read as machine-written: a language model picks the continuation that suits the
widest range of readers, so it reaches for words and shapes that signal importance,
balance and polish without committing to a specific claim. Human web copy written by
someone who knows the business is uneven and specific: it names the street, the price, the
customer, the reason. Every pattern below is a place where the general signal stands in
for the specific claim.

---

### AT-01 · Chatbot leftovers and knowledge-cutoff disclaimers

**Pass:** 1 · **Acts on:** one sighting

**Detect when**

- The text addresses the person who asked for it, not the page's reader: "Certainly!",
  "Sure, here is", "Great question", "I hope this helps", "Let me know if you'd like me to
  adjust the tone", "Feel free to customise this".
- The text talks about its own limits: "As of my last update", "as of my knowledge
  cutoff", "I don't have access to real-time data", "As an AI language model".
- Template placeholders survived: `[Your Company Name]`, `[insert statistic]`,
  `{{city}}`, "Lorem ipsum" in body copy.
- A disclaimer hedges dates that the business itself would know: "While specific details
  may vary, the company was likely founded in the early 2000s."

**Not a tell when**

- The page is a genuine chat transcript, FAQ written in a support voice ("Sure! You can
  return items within 30 days") or an AI product's own documentation describing its model.
- "Feel free to contact us" addressed to the site visitor is ordinary web copy.

**Fix:** Delete the leftover. If a placeholder or guessed fact sits where a real detail
belongs, replace it with an owner question, never a guess.

| Before | After |
| --- | --- |
| Certainly! Here is an overview of our services. | (delete) |
| I hope this helps you choose the right plan! | (delete) |
| As of my last update, we offer three membership tiers. | We offer three membership tiers. |
| Founded in [Year], [Company Name] has grown steadily. | Founded in [owner: year], [owner: company name] has grown steadily. |
| The company was likely established in the early 2000s. | The company was established in [owner: year]. |
| Let me know if you would like a shorter version. | (delete) |

**Example**

> Before: Certainly! Below is a description of our bakery. As of my last update, we are
> open six days a week.
>
> After: We are open six days a week.

---

### AT-02 · Throat-clearing openers and signposting

**Pass:** 1 · **Acts on:** one sighting

**Detect when**

- An opening sentence sets a scene about the world in general before the page says
  anything: "In today's fast-paced digital landscape", "In an ever-changing world", "In
  the modern era of", "Now more than ever".
- The text announces what it is about to do instead of doing it: "In this article, we will
  explore", "Let's dive in", "Let's take a closer look", "Without further ado", "Here's
  everything you need to know", "This guide will walk you through".
- A "whether you're X or Y" opener lists audiences instead of addressing the one reading:
  "Whether you're a seasoned pro or just starting out".
- A heading is immediately restated as the first sentence: "## Our Process" followed by
  "Our process is designed to...".

**Not a tell when**

- A long how-to or documentation page has a genuine table of contents or a one-line
  scope statement that tells readers what is and is not covered.
- "Whether you're X or Y" introduces a real fork that the page then handles differently
  for each group.

**Fix:** Delete the opener and start with the first real claim. If the heading restatement
carries a fact, keep the fact and drop the restatement.

| Before | After |
| --- | --- |
| In today's fast-paced digital landscape, a fast website matters. | A fast website matters. |
| In this article, we'll explore five ways to cut your energy bill. | (delete; the heading already says it) |
| Let's dive into the details. | (delete) |
| Whether you're a first-time buyer or a seasoned investor, our team can help. | Our team helps first-time buyers and investors. |
| Now more than ever, businesses need reliable IT support. | Businesses need reliable IT support. |
| Our Process: Our process is designed to make renovation simple. | Our Process: We price the job in writing before any work starts. *(only if the page states this; otherwise cut the restatement)* |

**Example**

> Before: In today's ever-evolving world of home improvement, choosing the right
> contractor can feel overwhelming. In this guide, we'll walk you through everything you
> need to know.
>
> After: Choosing a contractor is easier if you know what to ask. Here are the questions
> we answer before every job.
>
> *Note for reviewer: the second sentence needs the page to actually list those
> questions; if it does not, delete the sentence instead.*

---

### AT-03 · Stock AI vocabulary

**Pass:** 1 · **Acts on:** a cluster

**Detect when**

- Two or more words or phrases from the list below appear in the same paragraph, or three
  or more in any 300 words; or
- Any single phrase from the *always* list appears.

*Always list* (flag on one sighting): delve into, a rich tapestry, a testament to,
navigate the complexities, embark on a journey, ever-evolving landscape, in the realm of,
unlock the full potential, a symphony of, nestled in the heart of.

*Cluster list:* leverage, utilize, seamless(ly), robust, elevate, empower, foster,
showcase, holistic, synergy, dynamic, cutting-edge, game-changer, transformative,
meticulous(ly), intricate, pivotal, crucial, vital, landscape (figurative), realm,
ecosystem (figurative), journey (figurative), unlock, harness, streamline, bespoke,
curated, vibrant, comprehensive, innovative, additionally, moreover, furthermore.

**Not a tell when**

- The word is literal: landscape gardening, a robust (strong) material, a curated museum
  collection, an ecosystem in ecology, a journey in a travel itinerary.
- The word is the industry's own term: "holistic" in a holistic-medicine clinic,
  "bespoke" for tailoring, "leverage" in finance.
- The owner lists the word as a protected term or keyword.

**Fix:** Replace with the plain word, or better, with the specific thing the word was
covering for. If the sentence says nothing once the word is plain, cut the sentence.

| Before | After |
| --- | --- |
| We delve into the details of your tax return. | We go through your tax return line by line. |
| Our team leverages cutting-edge tools to streamline your workflow. | Our team uses [owner: tool names] to cut the steps in your workflow. |
| A rich tapestry of flavours | A mix of [owner: name two or three dishes or ingredients] |
| Embark on your fitness journey with us. | Start training with us. |
| We utilize a holistic approach. | We look at [owner: what, specifically] together. |
| Unlock the full potential of your data. | Get more out of your data. |
| Additionally, we offer free delivery. | We also deliver for free. |
| Our meticulous attention to detail | Our care over details *(or name the detail: "we re-measure every room")* |

**Example**

> Before: At Greenleaf Dental, we leverage cutting-edge technology to deliver a seamless,
> holistic patient journey.
>
> After: At Greenleaf Dental, we use digital X-rays and same-day crowns, so most
> treatment takes one visit.
>
> *Note for reviewer: "digital X-rays and same-day crowns" must come from elsewhere on the
> site; if the page never names the technology, the fix is "we use [owner: which
> technology?]".*

---

### AT-04 · Wordy filler constructions

**Pass:** 1 · **Acts on:** one sighting

**Detect when** a multi-word construction has a plain equivalent of one or two words and
the long form adds nothing:

- "in order to", "for the purpose of", "with the aim of"
- "due to the fact that", "owing to the fact that", "in light of the fact that"
- "it is important to note that", "it is worth mentioning that", "it should be noted that"
- "at this point in time", "at the present time", "in the event that"
- "has the ability to", "is able to" (where "can" works), "a wide range of", "a variety of
  different"
- "when it comes to", "in terms of" used as a sentence opener

**Not a tell when**

- The long form is needed for rhythm or clarity in a specific sentence ("In order to
  qualify, you must..." in a legal-ish eligibility notice is fine).
- It sits inside protected or legal text.

**Fix:** Compress to the plain form. Keep the rest of the sentence as it is.

| Before | After |
| --- | --- |
| in order to achieve this goal | to achieve this |
| due to the fact that our team is small | because our team is small |
| It is important to note that prices exclude VAT. | Prices exclude VAT. |
| Our app has the ability to sync across devices. | Our app syncs across devices. |
| We offer a wide range of different services. | We offer [owner: number or list] services. *or* We offer many services. |
| When it comes to pricing, we are transparent. | Our prices are listed on every product page. *(if true; otherwise: "We publish our prices.")* |
| In the event that your order is late, contact us. | If your order is late, contact us. |
| At this point in time, we are not accepting new clients. | We are not taking new clients right now. |

**Example**

> Before: It is worth noting that, in order to provide the best possible service, our
> technicians have the ability to work evenings due to the fact that many clients work
> during the day.
>
> After: Our technicians can work evenings, because many clients work during the day.

---

### AT-05 · Stacked hedges

**Pass:** 1 · **Acts on:** one sighting

**Detect when** one claim carries two or more softeners that weaken it in the same
direction: "may potentially", "could possibly", "might perhaps", "can often help to
somewhat", "generally tends to", "it could be argued that ... may", "in some cases ...
might".

**Not a tell when**

- The hedges are doing different jobs and both are true ("Most patients can usually
  return to work in a week" may be a clinically accurate double qualification; check
  before flagging).
- The text is medical, legal or financial and the hedge is a compliance requirement. Flag
  as protected if anything.

**Fix:** Keep the one hedge that matches the real uncertainty and drop the others. If the
claim is not uncertain at all, drop every hedge.

| Before | After |
| --- | --- |
| This may potentially reduce your costs. | This can reduce your costs. |
| It could possibly be argued that our approach might be faster. | Our approach is often faster. |
| Regular servicing can often help to somewhat extend the life of your boiler. | Regular servicing extends the life of your boiler. |
| Results may vary and might not always be guaranteed. | Results vary. |
| This generally tends to work well for most small businesses. | This works well for most small businesses. |

**Example**

> Before: Switching to LED lighting may potentially help to somewhat lower your energy
> bills over time.
>
> After: Switching to LED lighting lowers your energy bills over time.

---

### AT-06 · Avoiding "is" and "has"

**Pass:** 1 · **Acts on:** a cluster (two or more in one paragraph, or three on a page)

**Detect when** a dressed-up verb replaces a plain "is", "are" or "has":

- "serves as", "stands as", "acts as", "functions as" (where "is" works)
- "boasts", "features", "offers" (where "has" works and nothing is being sold)
- "represents", "constitutes", "marks" (where "is" works)

**Not a tell when**

- The verb is literal: a cafe "features" live music on Fridays, a deck "acts as" a roof for
  the patio below, a list "offers" products for sale.
- Only one occurs on the page.

**Fix:** Use is, are or has. If the sentence then reads as obviously empty, it was
probably also AT-07; rewrite around the specific fact.

| Before | After |
| --- | --- |
| The library serves as a hub for the community. | The library is the community's main meeting place. *(only if the page supports "main"; else "is a community meeting place")* |
| The hotel boasts 40 rooms and a rooftop pool. | The hotel has 40 rooms and a rooftop pool. |
| Our office stands as a symbol of our commitment to the city. | Our office is in the city centre. *(keep only what the page states)* |
| This update represents a major improvement. | This update is a major improvement. |
| The kitchen features granite countertops. | The kitchen has granite countertops. |

**Example**

> Before: The clinic boasts three treatment rooms and serves as the region's only
> specialist practice. It stands as a testament to Dr Patel's vision.
>
> After: The clinic has three treatment rooms and is the region's only specialist
> practice. Dr Patel opened it in [owner: year].
>
> *Also: AT-07 on the last sentence. The owner question replaces an empty claim with the
> fact readers would want.*

---

### AT-07 · Inflated significance and legacy

**Pass:** 2 · **Acts on:** one sighting

**Detect when** an ordinary fact is framed as historic, pivotal or symbolic without
anything to support the size of the claim:

- "plays a pivotal / crucial / vital role in", "a key turning point", "marks a significant
  milestone", "a defining moment"
- "stands as a testament to", "is a testament to", "a symbol of", "reflects our deep
  commitment to"
- "leaves a lasting legacy", "has left an indelible mark", "continues to shape the
  future of"
- "in the ever-evolving world of", "the broader landscape of", "the evolving landscape"

**Not a tell when** the page supplies the evidence for the size of the claim (a citation,
a date, a number, a named outcome). "The 1906 earthquake was a turning point for San
Francisco building codes" is a supported historical claim.

**Fix:** State the plain fact. If the significance matters, show it with the evidence the
page already has. If there is no evidence, drop the significance.

| Before | After |
| --- | --- |
| Our new warehouse marks a significant milestone in our journey. | We opened a new warehouse in [owner: place] in [owner: year]. |
| Customer service plays a pivotal role in everything we do. | We answer every email within one working day. *(if the page says so; else delete)* |
| The award stands as a testament to our team's dedication. | The team won [award name] in [year]. |
| This partnership reflects our deep commitment to sustainability. | Through this partnership we [owner: what changes, concretely]. |
| She left an indelible mark on the local arts scene. | She ran the town's gallery for 20 years. *(using facts already on the page)* |

**Example**

> Before: Founded in 1998, Lakeside Movers has played a pivotal role in shaping the
> moving industry in Ohio, and our growth stands as a testament to our unwavering
> commitment to excellence.
>
> After: Lakeside Movers has moved families around Ohio since 1998.

---

### AT-08 · Brochure language

**Pass:** 2 · **Acts on:** a cluster (two or more sales adjectives in one sentence, or
three in a paragraph)

**Detect when** a passage piles up generic praise adjectives that could describe any
business: nestled, vibrant, breathtaking, stunning, world-class, state-of-the-art,
unparalleled, unrivalled, second to none, premier, exceptional, unforgettable,
must-visit, hidden gem, one-stop shop, best-in-class, top-notch, unmatched.

**Not a tell when**

- One adjective is attached to a specific, checkable fact ("a stunning view of the
  harbour from every room").
- The page quotes a customer review (protected; leave it).

**Fix:** Swap the adjectives for the facts that would make a reader believe them: what,
where, how many, how fast, for whom. If the page has no such facts, cut to the plain noun
and add an owner question only if the gap is important.

| Before | After |
| --- | --- |
| Nestled in the heart of downtown, our vibrant cafe offers an unforgettable experience. | Our cafe is on Main Street, two minutes from the station. *(if stated)* |
| We provide world-class, state-of-the-art facilities. | Our gym has [owner: equipment or opening hours]. |
| An unparalleled selection of premium wines | Over 300 wines, most under $25. *(using page facts)* |
| Your one-stop shop for all your printing needs | We print business cards, banners and signs. |
| Experience breathtaking views and exceptional service. | Every room faces the lake. |

**Example**

> Before: Nestled in the picturesque countryside, our stunning venue offers an
> unparalleled setting for your unforgettable special day.
>
> After: Our venue is a converted barn on a working farm, with space for 120 guests.

---

### AT-09 · ", highlighting..." tails

**Pass:** 2 · **Acts on:** one sighting

**Detect when** a sentence ends with a participle clause that comments on the sentence's
own meaning rather than adding a fact: ", highlighting...", ", underscoring...",
", showcasing...", ", emphasizing...", ", reflecting...", ", ensuring...",
", contributing to...", ", fostering...", ", demonstrating...", ", solidifying its
position as...".

**Not a tell when** the "-ing" clause adds a separate, concrete fact or action: "We
inspect the roof, checking every tile for cracks" (the clause says what the inspection
does). Test: delete the clause. If no fact is lost, it was a tell.

**Fix:** Cut the tail. If it held a real fact, give that fact its own sentence or clause
with a real verb.

| Before | After |
| --- | --- |
| We donated 500 meals last winter, highlighting our commitment to the community. | We donated 500 meals last winter. |
| Our software encrypts all data, ensuring peace of mind for our clients. | Our software encrypts all data. |
| The firm won three regional awards, solidifying its position as a market leader. | The firm won three regional awards. |
| Classes are capped at eight, fostering a supportive environment. | Classes are capped at eight, so the instructor knows every student. *(if the page says so; else cut the tail)* |
| Sales grew 40%, reflecting strong demand. | Sales grew 40%. |

**Example**

> Before: The renovated lobby features local artwork, showcasing the hotel's dedication to
> the arts and reflecting the vibrant spirit of the city.
>
> After: The renovated lobby has paintings by local artists.

---

### AT-10 · "Not just X, it's Y" contrasts

**Pass:** 2 · **Acts on:** one sighting

**Detect when** a contrast sets up a claim nobody made so the real claim sounds larger:

- "It's not just X, it's Y", "X isn't just about A, it's about B"
- "not only X, but also Y" where X and Y are both vague
- "More than just a gym, it's a community"
- Split forms: "This isn't a sales pitch. It's a promise."
- Clipped tails: "Fresh bread daily, no shortcuts."

**Not a tell when**

- The first half corrects a belief readers really hold: "This is not a subscription: you
  pay once." (readers often expect a subscription).
- Both halves carry concrete information: "Not only do we install panels, we also handle
  the grid connection paperwork."

**Fix:** State the positive claim directly, with its specifics. Drop the straw half.

| Before | After |
| --- | --- |
| It's not just a haircut, it's an experience. | Every cut includes a wash and a scalp massage. *(if stated; else "We take our time with every cut.")* |
| More than just a gym, we're a community. | Members train together in small groups and meet monthly. *(if stated)* |
| This isn't just software. It's a partnership. | We assign you an account manager for the first year. *(if stated)* |
| We don't just fix computers; we build relationships. | We fix computers, and most of our customers have been with us for years. *(only if the page says so)* |
| Real ingredients, no compromises. | We make everything from fresh ingredients. |

**Example**

> Before: Our planning service isn't just about organizing events. It's about creating
> memories that last a lifetime.
>
> After: We plan weddings and corporate events, from the venue booking to the cleanup.

---

### AT-11 · Reflexive triads

**Pass:** 2 · **Acts on:** a cluster (three or more groups of three in a page, or two in
one paragraph)

**Detect when** items come in threes because three sounds complete, not because there are
three things: "fast, reliable and affordable"; "innovation, integrity and excellence";
"we listen, we learn, we deliver"; three near-synonyms in a row ("clear, concise and
easy to understand").

**Not a tell when** there really are three things and each is specific: "We serve
Leeds, York and Harrogate" or "Open Monday, Wednesday and Friday".

**Fix:** Keep the items that are specific and true; drop near-synonyms. Two items or one
is fine. Do not replace a triad with a different triad.

| Before | After |
| --- | --- |
| Our team is passionate, dedicated and committed. | Our team is committed. *(or name what they do)* |
| We offer fast, reliable and affordable service. | Most repairs are done the same day, from $49. *(if stated; else "We offer fast, affordable service.")* |
| Our values: innovation, integrity and excellence. | Our values: honest quotes and work we guarantee for a year. *(if stated)* |
| Clear, concise and easy-to-understand reports | Plain-English reports |
| We listen, we learn, we deliver. | We listen first, then quote. |

**Example**

> Before: We combine creativity, strategy and technology to deliver engaging, impactful
> and memorable campaigns that inspire, connect and convert.
>
> After: We plan and run social media campaigns for local retailers.

---

### AT-12 · Vague attribution

**Pass:** 2 · **Acts on:** one sighting

**Detect when** a claim leans on an unnamed authority: "experts agree", "studies show",
"research suggests", "industry reports indicate", "many believe", "it is widely
recognized that", "according to industry leaders", "customers say" with no customer.

**Not a tell when** the source is named or linked nearby on the page (same paragraph or a
footnote). Check the extracted blocks around the passage before flagging.

**Fix:** Either name the source (only if the page itself names it elsewhere) or drop the
attribution and make the claim in the business's own voice, if it can stand on its own.
If the claim needs a source to be honest, use an owner question. Never invent a study,
expert or statistic.

| Before | After |
| --- | --- |
| Studies show that regular massage reduces stress. | Many of our clients book a massage to help with stress. *(if true)* *or* Regular massage reduces stress [owner: source?]. |
| Experts agree that early planning saves money. | Planning early saves money: venues raise prices as dates fill. *(if the page says so)* |
| It is widely recognized that we are the leading provider in the region. | We have [owner: number] clients in the region. |
| Industry reports indicate rising demand for solar. | Solar installations in [region] rose [owner: figure and source]. |
| Many believe that handmade furniture lasts longer. | Handmade joints last longer than glued flat-pack joints. *(only if stated)* *or* (delete) |

**Example**

> Before: Research shows that 9 out of 10 homeowners prefer our windows, and experts agree
> they are the most energy-efficient on the market.
>
> After: [owner: where does the 9-in-10 figure come from? If there is no source, delete
> it.] Our windows are rated [owner: energy rating].
>
> *Note for reviewer: unsupported statistics on a sales page can be a legal problem, not
> just a style one.*

---

### AT-13 · Generic upbeat conclusions

**Pass:** 2 · **Acts on:** one sighting

**Detect when** a closing sentence or paragraph restates the page in general, optimistic
terms and adds nothing: "In conclusion", "In summary", "Ultimately", "The future looks
bright", "exciting times ahead", "the possibilities are endless", "With the right
partner, anything is possible", "we look forward to continuing this journey together".
Also the same upbeat closer at the end of several sections.

**Not a tell when** the ending carries a real next step (a call to action with a phone
number, a booking link, a deadline) or a concrete summary of a long technical page.

**Fix:** Cut it, or replace it with the actual next step the page already offers.

| Before | After |
| --- | --- |
| In conclusion, choosing the right roofer is essential for your home. | (delete) |
| The future looks bright, and we can't wait to see what's next! | (delete) |
| Ultimately, with the right partner, the possibilities are endless. | Call us on [number on page] for a free quote. |
| We look forward to continuing this journey together. | (delete) |
| In summary, our services help businesses thrive. | (delete; or a one-line call to action the page already has) |

**Example**

> Before: In conclusion, a well-maintained garden is a source of joy for years to come.
> With our expert team by your side, the possibilities are truly endless.
>
> After: Book a free garden visit at the link below.
