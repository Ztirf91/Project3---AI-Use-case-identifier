# AI Use Case Brief: Riese & Müller

12 November 2026 · [https://www.r-m.de](https://www.r-m.de)

> Prepared from public sources before a first conversation. Statements marked *documented* link to their source. Statements marked *assumption* describe what companies of this kind usually do. They are hypotheses for the meeting, not facts about Riese & Müller.

## 1. The company

**Premium e-bike and e-cargo bike manufacturer selling mainly through specialist dealers, with an added connected-service and business/fleet offering.**

### Business model

- Customers pay for premium e-bikes, e-cargo bikes, accessories, services, and connected-bike features through the specialist dealer channel and the company website’s dealer locator / service pages. *([documented](https://www.r-m.de/de/))*
- Dealers are the main sales and service channel: they advise customers, arrange test rides, and handle maintenance/in-service support. *([documented](https://www.r-m.de/de/))*
- The company also sells to business customers with premium bikes for fleet and sharing use cases. *([documented](https://www.r-m.de/de/))*
- In the US, the company is exiting the market, so revenue focus shifts further toward European core markets and the dealer network there. *([documented](https://www.bicycleretailer.com/industry-news/2026/04/20/riese-m%C3%BCller-will-leave-us-market-july))*
- It monetizes connected-bike services through RX Connect, including features such as trip tracking, location, insurance, and theft protection; some models include this in the first year. *([documented](https://www.r-m.de/de/ueber-uns/))*

### Unit economics

- The earning unit is a configured premium bicycle or cargo bike sold through dealers; margin is driven by premium pricing, configuration mix, and component quality. *([documented](https://www.r-m.de/de/))*
- Service and connected-bike add-ons increase lifetime value beyond the initial bike sale, especially through registration, insurance, and digital features. *([documented](https://www.r-m.de/de/ueber-uns/))*
- Because the company assembles in Germany and emphasizes quality standards, margin is likely sensitive to labor, component cost, and manufacturing efficiency. *([documented](https://www.r-m.de/de/ueber-uns/))*
- Dealer network reach and market focus affect volume and demand generation; the US exit indicates that market economics can change the profitable mix by region. *([documented](https://www.bicycleretailer.com/industry-news/2026/04/20/riese-m%C3%BCller-will-leave-us-market-july))*

### Preliminary process overview

Working hypothesis from public sources; validate with the company.

![Process map for Riese & Müller](riese-mueller-process-map.png)

- **1. Customers discover bikes, accessories, and business offers via the website and dealer network** · website / dealer locator · *([documented](https://www.r-m.de/de/))*
- **2. Specialist dealers advise, demo, and help customers choose a configuration** · dealer channel · *([documented](https://www.r-m.de/de/))*
- **3. Orders are accepted and routed through the dealer sales network in Europe** · dealer portal / email · *([documented](https://www.r-m.de/de/))*
- **4. Bikes are designed and assembled in Germany to company quality standards** · ERP / production systems · *([documented](https://www.r-m.de/de/ueber-uns/))*
- **5. Finished bikes are handed over through dealers and can be registered in the customer’s Mein Bike account** · dealer process / customer account · *([documented](https://www.r-m.de/de/))*
- **6. RX Connect digital services activate tracking, location, insurance, and theft protection for eligible models** · app / connected service platform · *([documented](https://www.r-m.de/de/ueber-uns/))*
- **7. Dealers provide aftersales maintenance and in-service support** · dealer workshop / service ticketing · *([documented](https://www.r-m.de/de/))*
- **8. Marketing and paid media generate international demand and leads** · ad platforms / analytics · *([documented](https://jobs.r-m.de/job/M%C3%BChltal-Senior-Manager-Paid-Media-&-Performance-Marketing-%28mwd%29/1362995955/))*

### Where AI fits in this business

Riese & Müller should use AI to remove friction in the dealer-facing core, not to replace the dealer-led premium selling model. The near-term priority is to protect margin and volume in Europe after the U.S. exit by making order intake, service activation, and marketing operations cheaper and faster. That fits a business where revenue depends on premium configuration quality, dealer throughput, and add-on lifetime value. The company already has structured processes and digital touchpoints, so the best first move is to redesign narrow workflow steps and let AI draft, extract, or classify where the data is explicit. Human-led steps with tacit judgment—dealer advice, assembly, and aftersales diagnosis—should stay human-led for now because the error cost is high and the premium brand depends on trust and quality.

**Leave alone for now**

- Specialist dealers advise, demo, and help customers choose a configuration — high error cost and tacit product-fit judgment make this a human-led premium-selling step.
- Bikes are designed and assembled in Germany to company quality standards — quality and safety risk are too high for end-to-end AI automation.
- Dealers provide aftersales maintenance and in-service support — fault diagnosis and customer trust rely on tacit expertise, so AI should only assist later if at all.

## 2. Three use cases

### 1. Triage dealer order emails into structured order drafts

**Process step:** Orders are accepted and routed through the dealer sales network in Europe · **Approach:** redesign then automate · **Lever:** more units sold · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Define one intake owner, standardize the required order fields, and remove free-form back-and-forth for incomplete dealer requests before AI touches the process. Then let AI extract order data from emails and attachments into a draft order that the team verifies.

**How the work runs afterwards.** A dealer order email or PDF triggers extraction into a structured draft. AI pulls bike model, options, quantities, dealer details, and missing fields; the order team checks exceptions, pricing, and availability before submission to ERP or the dealer portal.

**Money effect.** At ~40 dealer order requests/day and ~5 minutes saved per request from the card pattern (assumption), this saves about 3.3 hours/day, or roughly 850 hours/year at 260 working days. If the real volume is higher, the savings scale directly with order count.

**Reference.** Adapted from "Interpret emailed orders and quotation requests" ([Google Cloud / Danfoss](https://cloud.google.com/customers/danfoss?hl=zh-TW)); customer case study.

**Pilot.** Baseline: current minutes per order and error rate in dealer order intake. Success measure: minutes per order and erroneous order entries, using the card’s pilot metrics. Owner: dealer sales operations lead. Scale when structured drafts are accepted reliably and exception rates stay below the current manual baseline.

### 2. Automate RX Connect activation checks and exception handling

**Process step:** RX Connect digital services activate tracking, location, insurance, and theft protection for eligible models · **Approach:** quick win · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Keep activation exceptions out of the main flow by standardizing the activation checklist and naming an owner for missing serial numbers, consent flags, or service eligibility. Then use AI to validate incoming activation records, classify issues, and prepare the activation packet for human approval.

**How the work runs afterwards.** When a bike is sold or registered, the activation request enters a monitored queue. AI checks whether the serial number, model eligibility, and activation data are complete, flags gaps, and drafts the activation outcome; the service team only handles exceptions or approves edge cases.

**Money effect.** If the company processes ~120 connected-service activations/day (assumption) and AI saves ~2 minutes of manual checking per activation, that frees about 4 hours/day, or roughly 1,000 hours/year at 250 working days. The value is lower rework and lower handling cost for a repetitive post-sale task.

**Reference.** Adapted from "Maintain an operational dashboard from approved exports" ([OpenAI / ChatGPT use cases](https://learn.chatgpt.com/use-cases/analyze-data-export)); workflow guide.

**Pilot.** Baseline: current activation handling time and exception rate. Success measure: source freshness is not the main KPI here; use handling time and incorrect recommendations from the card’s metrics. Owner: connected services operations lead. Scale when the exception rate stays stable or drops and the verification workload is clearly lower than today.

### 3. Draft and localize campaign variants for European demand generation

**Process step:** Marketing and paid media generate international demand and leads · **Approach:** quick win · **Lever:** more units sold · **Human role:** Creative catalyst (AI proposes, a person chooses)

**Change the process first.** Narrow the workflow to approved product facts and a single campaign brief per region, then standardize the input format so AI does not have to infer claims or positioning. Let AI generate ad copy variants and calls to action; a marketer chooses the best ones and sends them into test and approval.

**How the work runs afterwards.** A campaign brief or product launch triggers copy generation. AI produces multiple ad variants, headline options, and CTA drafts in the brand voice; the marketing manager reviews, selects, and adapts them for the target market before launch.

**Money effect.** If the team currently needs ~30 minutes to draft and adapt one paid-media variant and AI cuts that to ~10 minutes, then each variant saves ~20 minutes. At ~25 variants/week (assumption), that is about 8.3 hours/week, or roughly 430 hours/year.

**Reference.** Adapted from "Generate ad copy and calls to action" ([n8n](https://n8n.io/workflows/4372-generate-product-ad-copy-and-ctas-with-gpt-4-for-slack-and-airtable/)); workflow template.

**Pilot.** Baseline: current hours to produce approved variants and current conversion in controlled tests. Success measure: approved variants per hour and conversion in controlled tests, per the card. Owner: performance marketing lead. Scale when the team can produce more approved variants without increasing correction rate or lowering lead quality.

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

**Dealer demand cockpit for premium Europe**

*Speculation for the meeting — not one of the three library-backed use cases above.*

**Today.** Marketing, dealer feedback, and order signals are likely reviewed in separate tools and meetings, so teams can see what happened but not easily turn it into a live regional opportunity picture.

**Redesigned with AI.** Combine dealer inquiries, campaign performance, web interest, and order signals into an AI-assisted demand cockpit that suggests which region, bike category, and message to prioritize next. Humans would use it to choose launches, allocate dealer support, and spot weak regions earlier than before.

**New capability.** The company could make faster regional demand decisions and create a new premium dealer-support service: a shared, insight-driven planning view for the European network.

**Business value if true.** If better regional allocation lifts conversion or reduces wasted media by even 1-2% on European demand spend, it could improve volume while protecting margin after the U.S. exit. The bigger upside is earlier detection of weak demand pockets and better dealer support decisions, not labor replacement.

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

- How many dealer order requests and RX Connect activations do you handle per day or week in Europe, and through which channels do they arrive today?
- Who owns exceptions today for dealer order intake and for connected-service activation issues, and where do those decisions get made?
- What exact fields are required to accept a dealer order, and how often are requests missing one or more of those fields?
- How many minutes does a person currently spend on one order intake case and one RX Connect activation case, including follow-up for missing information?

### Numbers to ask for

- Exact annual revenue
- Bike units sold per year
- Share of sales by Germany vs other European markets
- Share of revenue from accessories, services, and RX Connect
- Dealer count by country beyond the stated total of around 1,400
- Employee count trend beyond more than 700 employees

### Gaps in the public research

- Dropped 1 job posting(s) without a clear process signal.
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

- [Riese & Müller | Premium Bikes](https://www.r-m.de/de/)
- [Über uns | Riese & Müller](https://www.r-m.de/de/ueber-uns/)
- [Riese & Müller | Jobs](https://www.r-m.de/de/jobs/)
- Job posting: [Ausbildungsplatz als Fachkraft für Lagerlogistik (m/w/d) - Start 2027](https://jobs.r-m.de/job/M%C3%BChltal-Ausbildungsplatz-als-Fachkraft-f%C3%BCr-Lagerlogistik-%28mwd%29-Start-2027/1371327755/)
- Job posting: [Ausbildungsplatz als Fahrradmonteur (m/w/d) - Start 2027](https://jobs.r-m.de/job/M%C3%BChltal-Ausbildungsplatz-als-Fahrradmonteur-%28mwd%29-Start-2027/1371311955/)
- Job posting: [Senior Manager Paid Media & Performance Marketing (m/w/d)](https://jobs.r-m.de/job/M%C3%BChltal-Senior-Manager-Paid-Media-&-Performance-Marketing-%28mwd%29/1362995955/)
- News: [Riese & Müller will leave US market in July | Bicycle Retailer and Industry News](https://www.bicycleretailer.com/industry-news/2026/04/20/riese-m%C3%BCller-will-leave-us-market-july)
- News: [Riese & Müller Superdelite5 in Review: The Best SUV eBike Of 2026 With Everything You Need? | E-MOUNTAINBIKE Magazine](https://ebike-mtb.com/en/the-best-suv-trekking-e-bike-review/riese-mueller-superdelite5)
- News: ["Persistently challenging and increasingly volatile market conditions" – premium ebike brand withdraws from US market despite tariff relief  | BikeRadar](https://www.bikeradar.com/news/riese-and-muller-us-market-withdrawl)
- News: [Riese & Müller news for 2027: cargo bike updates and a brand-new urban bike - urbanbike.news](https://urbanbike.news/en/riese-muller-news-2027-cargo-bike-updates-new-urban-bike)
