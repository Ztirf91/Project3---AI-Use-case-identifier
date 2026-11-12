# AI Use Case Brief: Ankerstein

13 November 2026 · [https://anker-bausteine.de](https://anker-bausteine.de)

> Prepared from public sources before a first conversation. Statements marked *documented* link to their source. Statements marked *assumption* describe what companies of this kind usually do. They are hypotheses for the meeting, not facts about Ankerstein.

## 1. The company

**German manufacturer and online seller of handcrafted natural-material building toys and educational model kits.**

### Business model

- Customers pay for physical Ankerbausteine, starter sets, themed play sets, architecture models, and accessories sold on the company website. *([documented](https://anker-bausteine.de))*
- The company also monetizes special products such as limited editions and custom or made-to-order stones, which are excluded from withdrawal rights. *([documented](https://anker-bausteine.de/zeiss-planetarium-jena-anker-sonderbaukasten/0058952))*
- Revenue is generated through direct-to-consumer e-commerce, with orders shipped within Germany and free-shipping promotions above a stated basket threshold. *([documented](https://anker-bausteine.de))*
- The company additionally offers paid or value-adding services around the products, including workshops for educators, factory tours, and lending stones for events. *([documented](https://anker-bausteine.de/staunen/ueber-uns/))*

### Unit economics

- The earning unit is a sold set or special kit; margin depends mainly on selling price versus handcrafted production cost in Rudolstadt. *(assumption)*
- Margin is supported by product mix: higher-priced architecture sets, bundles, and special editions can carry better contribution than starter sets. *([documented](https://anker-bausteine.de))*
- Cost per unit is driven by natural raw materials, manual fabrication, precise quality requirements, and packaging/shipping. *([documented](https://anker-bausteine.de/staunen/ueber-uns/))*
- Risk is tied to inventory and made-to-order products, since custom items are excluded from withdrawal and likely need tighter planning. *([documented](https://anker-bausteine.de/en/revocation))*

### Preliminary process overview

Working hypothesis from public sources; validate with the company.

![Process map for Ankerstein](ankerstein-process-map.png)

### Where AI fits in this business

For Anker Bausteine, AI should be used first where the company already has explicit, repeatable information and where small speed gains can support sales or reduce labor per order. Because the business sells physical sets direct-to-consumer and also runs workshops and special products, the near-term prize is not full automation of the handcrafted core, but tighter support work around marketing, order intake, and warehouse operations. The current news points to product updates and newsletter activity, so improving content throughput can directly support demand generation without changing the product itself. In operations, AI should help standardize and surface exceptions, not replace tacit decisions in production or event delivery.

**Leave alone for now**

- Production team makes handcrafted Ankerbausteine in Rudolstadt — tacit craft knowledge and high defect cost make it a poor automation target now.
- Team runs factory tours, educator workshops, and event lending of stones — this is relationship-heavy, custom, and high judgment work; AI should stay assistive only.
- Quality control checks dimensional accuracy and compatibility — the error cost is high, so keep human verification rather than automating the decision.

## 2. Three use cases

### 1. Draft newsletter and promo variants from approved product updates

**Process step:** Marketing publishes newsletters, promotions, and product updates · **Approach:** quick win · **Lever:** more units sold · **Human role:** Creative catalyst (AI proposes, a person chooses)

**Change the process first.** Define one owner for each campaign, use a short approved source pack (product facts, offer rules, brand tone), and remove ad hoc rewriting from scratch before AI drafts variants.

**How the work runs afterwards.** When a product update, offer, or seasonal theme is approved, AI drafts newsletter copy and a few subject-line/options from the source pack; the marketer chooses the best angle, edits claims, and sends for approval before scheduling.

**Money effect.** At roughly 4 campaigns/month and about 45 minutes of drafting and rework each today (assumption), this can save about 3 hours/month per marketer and let the team publish more timely promos.

**Reference.** Adapted from "Repurpose approved long-form content for several channels" ([Zapier / Blog content repurposing](https://zapier.com/templates/details/repurpose-blog-content-across-channels)); workflow template.

**Pilot.** Baseline: current campaign prep time and approval cycle. Success measure: preparation hours per campaign, approved adaptations, and click or referral conversion. Owner: marketing lead. Scale when the team can produce on-brand drafts with no factual corrections and unchanged or better engagement.

### 2. Turn webshop support emails into draft replies

**Process step:** Customers browse themed sets and place orders on the webshop · **Approach:** quick win · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Separate simple, recurring webshop questions from exceptions, maintain a small approved FAQ set, and assign one owner for review so AI only handles the standard cases first.

**How the work runs afterwards.** A webshop or mailbox trigger sends routine questions about shipping, availability, or product basics to AI; it drafts a reply from approved answers, and staff verify anything about orders, returns, or special products before sending.

**Money effect.** At about 15 support emails/day and 4 minutes to triage and draft each reply today (assumption), this frees roughly 1 hour/day and reduces time spent on repetitive customer questions.

**Reference.** Adapted from "Draft FAQ answers from approved support content" ([n8n](https://n8n.io/workflows/4279-automated-email-sorting-and-drafting-for-customer-support-with-ai/)); workflow template.

**Pilot.** Baseline: current handling time and correction rate for support emails. Success measure: minutes per reply, factual accuracy, and share of messages resolved on first pass. Owner: customer service lead. Scale when standard questions are answered correctly with faster turnaround and no rise in complaint rate.

### 3. Rebalance packing work and layout from measured movement data

**Process step:** Packing team assembles boxes, inserts leaflets, and prepares recyclable packaging · **Approach:** redesign then automate · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Map the packing flow first, remove unnecessary walking and double-handling, standardize the sequence of inserts and packing materials, and then use AI to propose layout and task routing changes.

**How the work runs afterwards.** After a time-and-motion baseline is captured, AI analyzes packing movements and suggests a better station layout or picking sequence; supervisors test the change, and packers keep verifying that the box contents and leaflet set are correct.

**Money effect.** If packing and internal movement consume even 2 staff hours/day now (assumption), a layout change that cuts travel and waiting by 15-20% could save about 6-8 hours/month and raise throughput in peak periods.

**Reference.** Adapted from "Improve picking routes and warehouse layout" ([Plattform Lernende Systeme / META-Regalbau](https://www.plattform-lernende-systeme.de/booklet-include-elemente.html)); customer case study.

**Pilot.** Baseline: travel time per pack and orders packed per hour. Success measure: reduced travel time, stable error rate, and higher throughput. Owner: warehouse/picking supervisor. Scale when the new layout improves flow without increasing packing mistakes or delays.

## 3. Redesign the work, then apply AI

Do not automate the process as found — redesign it first. AI on yesterday’s workflow usually speeds up waste: retyping, handoffs, and approvals that should not exist. Break the work into tasks, cut or relocate what nobody needs, then decide what AI drafts or proposes and what a named person still owns. Ask which process to clean up first, and which human capabilities should get stronger afterward — not merely what can be automated.

Redesign pays when it moves unit economics, not when it saves a few clicks. Remove double entry and cycle time falls; standardize intake and errors fall; give specialists AI-prepared options and they spend time on judgment and customers. People stay accountable for money, legal, and customer outcomes; AI removes low-value motion around them. That is how AI becomes a complement instead of a faster broken process.

There are two ways to use AI in that redesign:

- **Option A — Automate / substitute.** AI copies what people already do and takes over those tasks. Machines become substitutes for labor. Output can get cheaper, but people become more replaceable and more of the upside goes to whoever owns the system.
- **Option B — Augment / complement.** AI enables people to do things they could not do before. Humans and machines are complements. Augmentation also tends to create new products, services, and tasks — not only cheaper versions of old ones.

This brief’s speculative redesign below is written as **Option B**.

**How we redesign with AI**

**Pattern we use in every brief**

| Step | Question | AI role | Human role |
|------|----------|---------|------------|
| 1. Purpose | What business outcome is this step for? | — | Name the lever (volume, price, unit cost, risk) |
| 2. Eliminate | What can disappear? | Flag duplicate/low-value steps from logs or samples | Cut re-entry, status theatre, unused approvals |
| 3. Standardize | One path in? | Enforce fields / classify intake | One exception owner |
| 4. Redesign flow | What is the new happy path? | Draft, retrieve, propose | Decide, commit money/customer/legal outcomes |
| 5. Pilot | Did a metric move? | Run on one queue/team | Baseline → compare → scale or stop |

**Business-value test.** Ship the redesign only if a named owner can point to a unit-economics lever and a baseline number to improve in the first meeting.

### Speculative case (Option B — augment / complement)

**Personalized build-play guidance from orders and age groups**

*Speculation for the meeting — not one of the three library-backed use cases above.*

**Today.** The webshop sells themed sets and age-based products, but customers largely choose from static pages and generic newsletters. The company has workshops and educator-facing products, yet those offers are not turned into individualized guidance at scale.

**Redesigned with AI.** Use AI to combine browsing behavior, age stage, and product families into a guided play advisor that suggests the next set, a classroom use idea, or a themed bundle. A human team would define the pedagogy and product rules, while AI generates tailored recommendations and short explanations for each visitor or educator segment.

**New capability.** The company could offer a more personal buying and learning experience: not just a catalog, but a guided selection service that helps parents and educators choose the right stone set for a child, classroom, or event.

**Business value if true.** Higher basket value and better repeat purchase rates from more relevant bundles, plus a clearer bridge from products to paid workshops and educator services.

## 4. Questions for the first meeting

### How to approach the conversation

As an AI consultant, start from the business, not from the tool: what the company wants to achieve, what blocks that, and which knowledge it can put to work — how it earns money, where cost and errors pile up, how work really runs, and where useful data and experience live (systems, files, or people’s heads). Only then ask where AI can connect information, create options, or take on steps — and which measurable result would prove the change was worth it.

### General questions

- What would “success in 12 months” look like in one sentence?
- Where do cost, delays, rework or complaints hurt most — and who owns that?
- Where does critical know-how live today, and how hard is it to find and trust?
- Who would own a first pilot, and which one metric would convince leadership?

### Use-case questions

Ordered by: without an answer, there is no pilot.

- How many newsletter or promo campaigns do you actually send in a typical month, and who is the single approver for claims, pricing, and tone?
- Roughly how many webshop support emails do you get per day, and what share are simple shipping or availability questions versus exceptions?
- For packing, do you already track time spent walking or waiting between stations, or would we need a one-week baseline before changing the layout?
- What is the current average time per campaign draft, support reply, and packed order so we can test whether the pilot saves enough hours to matter?

### Numbers to ask for

- Exact annual output or sales volume
- Share of revenue from webshop versus workshops/tours/lending
- Average order value and repeat purchase rate
- Gross margin by product family
- Share of made-to-order versus stocked items
- Export share outside Germany

### Gaps in the public research

- No register or size information found.

## 5. How these use cases were chosen

Every process step was rated against a rubric (money lever, HBR human role, opportunity type, full cost, feasibility, redesign-before-AI, augment vs substitute). The strongest steps were matched to a curated library via retrieval and company-fit reranking; three cards were adapted to this company.

- [APQC, How Can Organizations Identify And Prioritize Valuable AI Use Cases?](https://www.apqc.org/How-Can-Organizations-Identify-And-Prioritize-Valuable-AI-Use-Cases)
- [AWS, Taxonomy of agentic primitives in Amazon Quick (2026)](https://aws.amazon.com/blogs/machine-learning/taxonomy-of-agentic-primitives-in-amazon-quick/)
- [Anand and Wu, The Gen AI Playbook for Organizations, HBR (2025)](https://hbr.org/2025/11/the-gen-ai-playbook-for-organizations)
- [OpenAI, Identifying and scaling AI use cases](https://openai.com/business/learn/identifying-and-scaling-ai-use-cases/)
- [appliedAI, How to find and prioritize AI use cases (2020)](https://www.appliedai.de/uploads/files/Whitepapers/appliedAI-Whitepaper-Applying-AI-How-to-find-and-prioritize-AI-use-cases-2020-EN.pdf)
- [MIT Sloan, How to find the right business use cases for generative AI (2025)](https://mitsloan.mit.edu/ideas-made-to-matter/how-to-find-right-business-use-cases-generative-ai)
- [Taylor Radey, Finding AI use cases: one helpful framework to try (2025)](https://www.taylorradey.com/post/finding-ai-use-cases-framework)
- [MIT Sloan, Want AI-Driven Productivity? Redesign Work](https://sloanreview.mit.edu/article/want-ai-driven-productivity-redesign-work/)
- [MIT Sloan, Don’t Let Artificial Intelligence Supercharge Bad Processes](https://sloanreview.mit.edu/article/dont-let-artificial-intelligence-supercharge-bad-processes/)
- [HBR, The Secret to Successful AI-Driven Process Redesign (2025)](https://hbr.org/2025/01/the-secret-to-successful-ai-driven-process-redesign)
- [HBR, Stop Automating Old Processes. Design New Ones Instead. (2026)](https://hbr.org/2026/09/stop-automating-old-processes-design-new-ones-instead)
- [Randstad, Before you automate, AI-vate or agent-icate](https://www.randstadenterprise.com/insights/randstad-enterprise-insights/before-you-automate-ai-vate-or-agent-icate/)
- [Brynjolfsson, The Turing Trap, Stanford Digital Economy Lab (2022)](https://digitaleconomy.stanford.edu/news/the-turing-trap-the-promise-peril-of-human-like-artificial-intelligence/)

## 6. Sources

- [Ankerstein Bausteine | Nachhaltige Bau- und Lernspielzeuge made in Germany | Ankerstein GmbH](https://anker-bausteine.de)
- [Ankerstein GmbH – Traditionelles Spielzeug aus Rudolstadt seit 1880 | Ankerstein GmbH](https://anker-bausteine.de/staunen/ueber-uns/)
- [Zeiss-Planetarium Jena aus Ankerbausteinen | Jubiläumsedition | Ankerstein](https://anker-bausteine.de/zeiss-planetarium-jena-anker-sonderbaukasten/0058952)
- News: [Anker Bausteine |](https://anker-bausteine.de/en/revocation)
