# AI Use Case Brief: Riese & Müller

12 November 2026 · [https://www.r-m.de](https://www.r-m.de)

> Prepared from public sources before a first conversation. Statements marked *documented* link to their source. Statements marked *assumption* describe what companies of this kind usually do. They are hypotheses for the meeting, not facts about Riese & Müller.

## 1. The company

**Premium e-bike and cargo bike manufacturer selling through dealers and serving B2C and B2B customers.**

### Business model

- Customers pay for premium e-bikes, cargo bikes, accessories, and related services such as warranty, insurance, and connected-bike features. *([documented](https://www.r-m.de/de/))*
- B2C buyers are served mainly through a dealer network for advice, test rides, handover, and maintenance rather than through a direct web shop. *([documented](https://www.r-m.de/de/))*
- B2B customers buy fleet and sharing solutions through Riese & Müller Business. *([documented](https://www.r-m.de/de/))*
- Employers and employees pay for job bike leasing offerings coordinated via the company’s leasing proposition. *([documented](https://www.r-m.de/de/))*
- The company focuses on European core markets and its dealer network after exiting the US market. *([documented](https://www.bicycleretailer.com/industry-news/2026/04/20/riese-m%C3%BCller-will-leave-us-market-july))*

### Unit economics

- The earning unit is a premium bicycle or cargo bike, with margin driven by product price, configuration options, and component quality. *([documented](https://www.r-m.de/de/ueber-uns/))*
- Margin is also influenced by manufacturing efficiency because the company assembles in Germany and runs a series-production operation. *([documented](https://www.r-m.de/de/ueber-uns/))*
- Connected-bike and after-sales services such as RX Connect, warranty extension, and insurance add recurring or attach revenue potential around the bike sale. *([documented](https://www.r-m.de/de/ueber-uns/))*
- Dealer-led sales and service shift some customer support and maintenance costs to the retailer network, supporting a lower direct-service burden for the manufacturer. *(assumption)*

### Current process map

| # | Step | Data in | Data out | Likely system | Basis |
|---|------|---------|----------|---------------|-------|
| 1 | Product management designs premium e-bikes and cargo bikes | Market feedback, design requirements, component options | Bike concepts and specifications | PLM | *([documented](https://www.r-m.de/de/ueber-uns/))* |
| 2 | Purchasing sources components from global partners | Specifications, bills of materials, supplier offers | Purchased parts and components | ERP | *([documented](https://www.r-m.de/de/ueber-uns/))* |
| 3 | Production team assembles bikes in Germany | Components, work orders, assembly instructions | Finished premium bikes | MES | *([documented](https://www.r-m.de/de/ueber-uns/))* |
| 4 | Quality team checks products against ISO standards | Finished units, test results, quality criteria | Quality approvals and nonconformance records | QMS | *([documented](https://www.r-m.de/de/ueber-uns/))* |
| 5 | Warehouse team receives and stores inbound goods | Incoming parts, delivery notes | Put-away inventory and stock records | WMS | *([documented](https://jobs.r-m.de/job/M%C3%BChltal-Sch%C3%BClerpraktikant-%28mwd%29/963222555/))* |
| 6 | Logistics team picks and stages parts for production | Stock locations, production demand | Picked kits and line-side supply | WMS | *([documented](https://jobs.r-m.de/job/M%C3%BChltal-Sch%C3%BClerpraktikant-%28mwd%29/963222555/))* |
| 7 | Sales team and dealers sell bikes to customers | Product portfolio, dealer inquiries, customer demand | Customer orders and dealer allocations | CRM | *([documented](https://www.r-m.de/de/))* |
| 8 | Order management processes production and delivery status | Orders, delivery milestones, customer emails | Status updates and delivery confirmations | ERP | *([documented](https://www.r-m.de/de/))* |
| 9 | Customer support handles questions, help-center requests, and warranty topics | Customer inquiries, warranty claims, service issues | Resolved cases and support responses | ticketing | *([documented](https://www.r-m.de/de/))* |
| 10 | Marketing team runs international paid media and brand campaigns | Media budgets, audience data, funnel metrics | Leads, traffic, conversions, campaign reports | CRM | *([documented](https://jobs.r-m.de/job/M%C3%BChltal-Senior-Manager-Paid-Media-&-Performance-Marketing-%28mwd%29/1362995955/))* |
| 11 | After-sales team manages connected-bike, insurance, and registration services | Bike registrations, connected-device data, insurance enrollment | Activated services and customer records | ticketing | *([documented](https://www.r-m.de/de/ueber-uns/))* |

### Where AI fits in this business

Riese & Müller should use AI first where it reduces service and order-handling cost without touching the core product promise. With the US exit and a sharper focus on European core markets, the priority is to make dealer-facing operations leaner and more reliable, not to automate high-risk design or quality decisions end to end. The best near-term wins are in structured, repetitive flows that already pass through ERP, CRM, WMS, and ticketing systems: dealer request intake, inbox routing, and warehouse movement analysis. These can lower unit cost and free staff time while preserving the human review that fits a premium, dealer-led brand. More strategic forecasting or product-design bets should wait until the company has cleaner demand and installed-base data across its core markets.

**Leave alone for now**

- Product management designs premium e-bikes and cargo bikes — design choices are tacit and high-stakes, so AI should not own concept decisions.
- Quality team checks products against ISO standards — error cost is high and the step is already control-oriented; keep humans leading inspections.
- After-sales team manages connected-bike, insurance, and registration services — this is customer-sensitive and high-error-cost work, so automate only small assistive pieces later.

## 2. Three use cases

### 1. Triage dealer and customer emails into order, service, and exception queues

**Process step:** Sales team and dealers sell bikes to customers · **Approach:** quick win · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Standardize a small set of intake categories for dealer emails and require every request to arrive in the shared inbox or portal with dealer ID, model, and country. Remove free-form retyping into CRM by routing the original message and extracted fields into one review queue.

**How the work runs afterwards.** Each incoming dealer or customer message triggers classification in the shared inbox. AI labels the request type, drafts the reply or next action, and extracts the key fields; a named sales operations owner reviews exceptions and approves outbound messages that affect pricing, allocation, or commitments.

**Money effect.** Cuts manual sorting and retyping time in dealer-facing sales operations, which matters now as the company refocuses on European dealer throughput after the US exit. Faster routing also reduces missed or delayed dealer responses, supporting volume without adding headcount.

**Why it fits.** This is repetitive, high-volume work with explicit categories, so it fits a quick win. The error cost is moderate to high because wrong routing can delay orders or promises, so the human must verify consequential replies. The company already works through dealer and service inboxes, so the process change is realistic without changing the business model.

**Reference pattern.** Adapted from "Shared inbox classification and routing" ([n8n](https://n8n.io/workflows/9157-ai-powered-email-triage-and-auto-response-system-with-openai-agents-and-gmail/)); workflow template.

**Source evidence.** Template classifies incoming mail and routes it to specialist agents. Publisher-reported; this does not establish the same outcome for this company.

**What has to be in place**

- A shared dealer inbox or ticket queue with stable message categories
- Named owners for sales, service, and order exceptions
- GDPR-compliant handling of personal data in customer and dealer messages

**Pilot.** Baseline: current minutes spent per message and routing error rate in the dealer sales inbox. Success measure: lower minutes per message and higher routing accuracy against the current baseline. Accountable owner: Head of Sales Operations. Scale when the pilot shows reliable category accuracy, fewer handoff delays, and no increase in missed or incorrect dealer commitments.

### 2. Convert inbound dealer order emails into ERP-ready quote and order drafts

**Process step:** Order management processes production and delivery status · **Approach:** redesign then automate · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Stop retyping dealer order content from email into ERP as a fully manual step. Require a single order template or structured attachment for the first intake step, and define one exception rule for price, configuration, or availability mismatches.

**How the work runs afterwards.** When an order email or attachment arrives, AI extracts the order details, matches them to the product catalog and dealer record, and creates a draft ERP order or quote. An order management specialist checks exceptions, confirms delivery milestones, and releases only clean cases into ERP.

**Money effect.** Reduces time spent converting messy dealer requests into usable orders and lowers entry errors that can trigger rework, returns, or delayed production planning. That matters more now because the company is concentrating on core European dealer operations and needs a tighter, lower-cost order flow.

**Why it fits.** The step is document-heavy and explicit, which makes extraction feasible, but the consequences of a wrong order are financially material, so human verification is required. This is a redesign because the current process contains a retyping workaround that should be removed before automation. It fits the company’s dealer-led model because the AI supports the back office without changing who sells to customers.

**Reference pattern.** Adapted from "Interpret emailed orders and quotation requests" ([Google Cloud / Danfoss](https://cloud.google.com/customers/danfoss?hl=zh-TW)); customer case study.

**Source evidence.** Danfoss reports 50% less processing time and about five minutes saved per order. Publisher-reported; this does not establish the same outcome for this company.

**What has to be in place**

- A current product catalog with dealer prices, configurations, and country rules
- ERP access for creating draft orders and quotes
- A named exception owner for price, availability, and configuration mismatches
- GDPR-compliant processing for dealer contact data and order documents

**Pilot.** Baseline: current minutes per order and the rate of erroneous order entries. Success measure: lower minutes per order and fewer erroneous entries versus the baseline. Accountable owner: Head of Order Management. Scale when draft accuracy is consistently high, exception handling is stable, and ERP rework drops without increasing delivery promises made to dealers.

### 3. Analyze warehouse movement data to redesign picking routes and staging layout

**Process step:** Logistics team picks and stages parts for production · **Approach:** redesign then automate · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**Change the process first.** Measure travel paths and waiting time before changing the layout or pick sequence. Standardize location data and define a fixed process owner who approves any relocation of fast-moving parts or line-side staging points.

**How the work runs afterwards.** The warehouse system or sensor data feeds AI analysis on travel distance, congestion, and staging delays. AI proposes a new pick sequence and slotting layout; the warehouse manager and team leads test the changes, keep the ones that reduce travel time, and reject changes that slow line feeding.

**Money effect.** Cuts non-value-added walking and waiting in internal logistics, which lowers labor cost per bike assembled in Germany. Because the company’s margin is tied to efficient serial production, even small time savings matter across a premium product mix.

**Why it fits.** Picking and staging are repetitive and data-rich, so this is a good fit for process redesign plus analysis. The error cost is not legal or customer-facing, but a bad layout change can hurt throughput, so a human owner must approve consequential moves. The company’s focus on manufacturing efficiency makes this more relevant than broader forecasting at this stage.

**Reference pattern.** Adapted from "Improve picking routes and warehouse layout" ([Plattform Lernende Systeme / META-Regalbau](https://www.plattform-lernende-systeme.de/booklet-include-elemente.html)); customer case study.

**Source evidence.** META-Regalbau reports about EUR 22000 annual savings from layout and logistics improvements. Publisher-reported; this does not establish the same outcome for this company.

**What has to be in place**

- Movement or scan data for warehouse picks and staging
- An up-to-date warehouse layout and location master data
- A warehouse owner who can approve slotting and routing changes
- GDPR and works-council review if worker movement data is used

**Pilot.** Baseline: current travel time per pick and line-side throughput. Success measure: lower travel time per pick and improved throughput versus the baseline. Accountable owner: Warehouse Manager. Scale when the pilot improves travel time without causing stock errors, congestion, or complaints from the team.

## 3. Questions for the first meeting

### 1. Triage dealer and customer emails into order, service, and exception queues

**Assumptions to test**

- Dealers still send most reorders and questions by email rather than through a structured portal.
- The inbox volume is high enough and categories stable enough to benefit from automated triage.
- Sales operations can own a review queue and enforce one standard intake path.

**Do you have this?**

- Do you have one shared inbox or ticketing queue for dealer sales requests today?
- Do you have a CRM field structure for dealer ID, country, product line, and request type?
- Do you have named people who can approve pricing, allocation, and exception replies?

**To decide whether this is the right use case**

- How many dealer or customer messages arrive per day or week, and how much time is spent sorting them now?
- What is the current routing or response error rate, and which mistakes hurt most: late replies, wrong allocation, or pricing errors?
- Who owns the inbox today, and where do messages most often get stuck?

### 2. Convert inbound dealer order emails into ERP-ready quote and order drafts

**Assumptions to test**

- Dealers still send many orders as unstructured email text or attachments rather than through a clean portal.
- The product catalog and dealer price list are current enough to match requests automatically.
- Order management can define one standard exception path instead of ad hoc back-and-forth.

**Do you have this?**

- Do you have a maintained product catalog with dealer pricing, options, and availability by market?
- Do you have an ERP integration point for creating draft quotes or orders from external inputs?
- Do you have a person or team that owns order exceptions and final release to production planning?

**To decide whether this is the right use case**

- How many inbound dealer orders or quote requests do you process each week, and how many require manual retyping?
- What is the current error rate in order entry, and how often do errors create downstream production or delivery issues?
- Who spends the most time on this step today: order management, sales ops, or dealer support?

### 3. Analyze warehouse movement data to redesign picking routes and staging layout

**Assumptions to test**

- The warehouse has enough scan or movement data to show where time is lost.
- Fast-moving parts and staging points can be rearranged without disrupting production.
- Warehouse staff will follow a revised pick route if the change is clearly better.

**Do you have this?**

- Do you have location-level warehouse data and pick scans for the main part families?
- Do you have a current layout map and material flow rules for the warehouse?
- Do you have a warehouse lead who can test and approve layout changes?

**To decide whether this is the right use case**

- How long does a typical pick or staging cycle take today, and where is the biggest delay?
- How much of warehouse time is spent walking versus handling parts?
- Who owns the layout decisions, and what is the current pain: labor cost, throughput, or missed line supply?

### Numbers to ask for

- Revenue, gross margin, and ASP per bike were not found.
- Installed base or annual unit volume were not found.
- Dealer count is given as about 1,400 on the company website, but channel split by region was not found.
- Employee count is given as more than 700 on the company website; a more current audited number was not found.

### Gaps in the public research

- No register or size information found.

## 4. How these use cases were chosen

Every process step was rated against a rubric drawn from public frameworks: the money lever it touches, error cost and type of knowledge (HBR), whether the task is repetitive, a bottleneck, or ambiguous (OpenAI, Taylor Radey), the full cost including human review (MIT Sloan), and feasibility in data, systems, and know-how (appliedAI). The most promising steps were matched against a curated library of customer cases, documented solutions, and workflow templates, and three were adapted to this company.

- [APQC, How Can Organizations Identify And Prioritize Valuable AI Use Cases?](https://www.apqc.org/How-Can-Organizations-Identify-And-Prioritize-Valuable-AI-Use-Cases)
- [AWS, Taxonomy of agentic primitives in Amazon Quick (2026)](https://aws.amazon.com/blogs/machine-learning/taxonomy-of-agentic-primitives-in-amazon-quick/)
- [Anand and Wu, The Gen AI Playbook for Organizations, HBR (2025)](https://hbr.org/2025/11/the-gen-ai-playbook-for-organizations)
- [OpenAI, Identifying and scaling AI use cases](https://openai.com/business/learn/identifying-and-scaling-ai-use-cases/)
- [appliedAI, How to find and prioritize AI use cases (2020)](https://www.appliedai.de/uploads/files/Whitepapers/appliedAI-Whitepaper-Applying-AI-How-to-find-and-prioritize-AI-use-cases-2020-EN.pdf)
- [MIT Sloan, How to find the right business use cases for generative AI (2025)](https://mitsloan.mit.edu/ideas-made-to-matter/how-to-find-right-business-use-cases-generative-ai)
- [Taylor Radey, Finding AI use cases: one helpful framework to try (2025)](https://www.taylorradey.com/post/finding-ai-use-cases-framework)

## 5. Sources

- [Riese & Müller | Premium Bikes](https://www.r-m.de/de/)
- [Über uns | Riese & Müller](https://www.r-m.de/de/ueber-uns/)
- [Riese & Müller | Jobs](https://www.r-m.de/de/jobs/)
- Job posting: [Ausbildungsplatz als Fachkraft für Lagerlogistik (m/w/d) - Start 2027](https://jobs.r-m.de/job/M%C3%BChltal-Ausbildungsplatz-als-Fachkraft-f%C3%BCr-Lagerlogistik-%28mwd%29-Start-2027/1371327755/)
- Job posting: [Ausbildungsplatz als Fahrradmonteur (m/w/d) - Start 2027](https://jobs.r-m.de/job/M%C3%BChltal-Ausbildungsplatz-als-Fahrradmonteur-%28mwd%29-Start-2027/1371311955/)
- Job posting: [Schülerpraktikant (m/w/d)](https://jobs.r-m.de/job/M%C3%BChltal-Sch%C3%BClerpraktikant-%28mwd%29/963222555/)
- Job posting: [Senior Manager Paid Media & Performance Marketing (m/w/d)](https://jobs.r-m.de/job/M%C3%BChltal-Senior-Manager-Paid-Media-&-Performance-Marketing-%28mwd%29/1362995955/)
- News: [Riese & Müller GmbH](https://tavily.com/knowledge/company/pd6f6kBV1oRW)
- News: [Riese & Müller will leave US market in July | Bicycle Retailer and Industry News](https://www.bicycleretailer.com/industry-news/2026/04/20/riese-m%C3%BCller-will-leave-us-market-july)
- News: [Riese & Müller Superdelite5 in Review: The Best SUV eBike Of 2026 With Everything You Need? | E-MOUNTAINBIKE Magazine](https://ebike-mtb.com/en/the-best-suv-trekking-e-bike-review/riese-mueller-superdelite5)
- News: ["Persistently challenging and increasingly volatile market conditions" – premium ebike brand withdraws from US market despite tariff relief  | BikeRadar](https://www.bikeradar.com/news/riese-and-muller-us-market-withdrawl)
- News: [Riese & Müller news for 2027: cargo bike updates and a brand-new urban bike - urbanbike.news](https://urbanbike.news/en/riese-muller-news-2027-cargo-bike-updates-new-urban-bike)
- News: [EXEC: Riese & Müller Hires CFO | SGB Media Online](https://sgbonline.com/exec-riese-muller-hires-cfo)
