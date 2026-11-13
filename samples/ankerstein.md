# AI Use Case Brief: Ankerstein

13 November 2026 · [https://www.ankerstein.de](https://www.ankerstein.de)

> Prepared from public sources before a first conversation. Statements marked *documented* link to their source. Statements marked *assumption* describe what companies of this kind usually do. They are hypotheses for the meeting, not facts about Ankerstein.

## 1. The company

**Inclusive manufacturer of Anker building stones in Rudolstadt, serving customers worldwide (S1).**

### Business model

- Ankerstein manufactures building toys for customers worldwide. The supplied source does not identify who buys directly, the sales channels, or individual export markets. *([documented](https://www.spielwarenmesse.de/en/mag/toy-lab/building-the-future-with-ankersteinen-for-140-years))*
- Revenue is likely earned from selling building-stone sets and related products; the supplied source does not disclose the product mix or commercial terms. *(assumption)*
- Arbeiterwohlfahrt Rudolstadt took over production in 2017 after threatened closure and subsequently operated Ankerstein GmbH as an inclusive business. The article reports ten employees. *([documented](https://www.spielwarenmesse.de/en/mag/toy-lab/building-the-future-with-ankersteinen-for-140-years))*
- The article reports a planned move to Rudolstadt's historic post office, requiring considerable renovation. The supplied excerpt does not establish whether the move was completed. *([documented](https://www.spielwarenmesse.de/en/mag/toy-lab/building-the-future-with-ankersteinen-for-140-years))*

### Unit economics

- The likely earning unit is a building-stone set sold. Its contribution depends on the realized selling price and the cost of materials, manufacturing labor, packaging, and fulfillment. *(assumption)*
- Production volume and saleable yield likely drive manufacturing cost per set: unused capacity, rejected stones, and rework spread costs over fewer saleable products. *(assumption)*
- Channel mix and shipping arrangements likely affect retained margin through intermediary discounts, delivery costs, and responsibility for international fulfillment. *(assumption)*

### Preliminary process overview

Working hypothesis from public sources; validate with the company.

![Process map for Ankerstein](ankerstein-process-map.png)

[Process details and evidence in the appendix](#appendix-process-details).

### Where AI fits in this business

Wave one should help Ankerstein's staff interpret orders, prepare material information and inspect stones within today's workflow, with people retaining consequential decisions. For the reported ten-person inclusive manufacturer, the aim is more capacity from existing staff and fewer defective products—not replacing craft work. The supplied article describes a substantial planned relocation, but its completion is unconfirmed and no current news is supplied; start with small pilots that avoid major systems changes. Larger process redesign is a later conversation, illustrated in section 3.

**Leave alone for now**

- The Rudolstadt manufactory produces Anker building stones — preserve the established manufacturing work; the evidence does not identify a suitable AI task here.
- Dispatch staff prepare outgoing orders for customers worldwide — retain human control of shipping commitments and destination-specific requirements until the actual channels and error costs are understood.

## 2. Three use cases

These three cases support the process as it runs today. Deeper redesign of the work is introduced in section 3.

### 1. Draft production requirements from incoming orders

**Process step:** Order-handling staff turn incoming orders into production and delivery requirements · **Approach:** quick win · **Lever:** lower cost per unit · **Human role:** Human first (a person leads, AI assists)

**How the work runs with AI.** When staff receive an order, they submit its text and attachments to AI, which extracts products, quantities and destinations into a draft matching the existing order record and highlights ambiguities. The order handler resolves product substitutions, delivery promises and missing details before recording anything. Start with copy-and-review support, not automatic system updates; this covers order interpretation, not inbox sorting or customer FAQ replies.

**Money effect.** Assuming 30 orders/week and 3 minutes net saved per order after review, this releases 90 minutes/week for order handling or customer follow-up. These are Ankerstein pilot assumptions, not the supplier case's results; released time is capacity, not automatically a payroll saving.

**Reference.** Adapted from "Interpret emailed orders and quotation requests" ([Google Cloud / Danfoss](https://cloud.google.com/customers/danfoss?hl=zh-TW)); customer case study.

**Pilot.** The order-handling lead owns a pilot on representative orders. Record baseline minutes per order and erroneous order entries; compare both with AI assistance, including review and correction time. Scale only if net handling time falls without increased consequential errors and staff can reliably resolve flagged exceptions.

### 2. Prepare the existing material-status summary

**Process step:** Production staff arrange materials needed to make building stones · **Approach:** quick win · **Lever:** lower cost per unit · **Human role:** Quality control (AI produces, a person verifies)

**How the work runs with AI.** At the current material-review point, production staff provide approved order and stock exports. AI refreshes the existing material-status summary, checks source dates and reconciles totals using agreed calculations, then flags discrepancies. Staff verify the summary and decide what to procure; AI neither forecasts demand nor places purchases. Begin with staff-triggered runs rather than a new scheduled system.

**Money effect.** Assuming staff currently spend 2 hours/week assembling this summary and AI reduces that effort by 50%, including verification, the saving is 1 hour/week. The pilot must also account for maintaining exports and correcting mismatches before treating this as a recurring reduction in administrative cost.

**Reference.** Adapted from "Maintain an operational dashboard from approved exports" ([OpenAI / ChatGPT use cases](https://learn.chatgpt.com/use-cases/analyze-data-export)); workflow guide.

**Pilot.** The production planning lead owns the pilot. Record baseline reporting hours, reconciliation errors and source freshness; measure the same indicators with AI assistance. Scale only if total preparation and checking effort falls, totals reconcile and stale sources are consistently flagged; otherwise park the case rather than redesign records as a pilot precondition.

### 3. Give quality staff a second look at stone surfaces

**Process step:** Production staff check stones and pack saleable products · **Approach:** strategic bet · **Lever:** less risk per unit · **Human role:** Human first (a person leads, AI assists)

**How the work runs with AI.** At the existing inspection point, a controlled camera captures stone surfaces and AI highlights suspected visible defects for the inspector. Quality staff still inspect, interpret natural variation and decide whether each stone is saleable; packing and package-content checks remain unchanged. The added image check could reveal small flaws staff otherwise overlook, but cannot certify hidden defects or toy safety.

**Money effect.** Assuming 1,000 stones inspected/week and a reduction of 2 escaped visible defects per 1,000 stones, the benefit would be 2 fewer defective stones reaching packing each week. This is a risk-reduction hypothesis, not a proven result; camera, labeling and review costs must be justified against avoided rework or complaints.

**Reference.** Adapted from "Inspect manufactured surfaces with computer vision" ([Plattform Lernende Systeme / elunic](https://www.plattform-lernende-systeme.de/best-practice.html?AID=959)); documented solution.

**Pilot.** The quality lead owns a shadow-mode pilot with no automatic rejection. Record baseline missed-defect rate, false rejects and inspection time using expert-reviewed samples. Scale only if testing on separate representative samples shows fewer missed visible defects without unacceptable false rejects or inspection delays, and the full operating cost is justified.

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

**Section 3 — Speculation: a build-design service using existing stones**

*Speculation for the meeting — not one of the three library-backed use cases above.*

**Today.** The supplied model describes producing stones and fulfilling product orders; it does not establish that Ankerstein offers customer-specific building designs.

**Redesigned with AI.** Option B for discussion: redesign selected customer engagements around a desired model rather than only a product order. AI and geometry-checking tools would propose constructions using the verified stone catalog; Ankerstein's experienced staff would refine feasibility, test builds and approve instructions before offering a design with the required sets.

**New capability.** Staff could explore many more construction alternatives and help customers turn an idea into a buildable model—potentially a new design service rather than faster order administration.

**Business value if true.** If customers value the service, it could increase sets sold per project or support a paid design offer. Validate willingness to pay and contribution after design, testing and support costs before investing.

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

- Who at Ankerstein will own order review and material-summary approval, and can they provide representative orders, a current catalog, stock exports and the material summary actually used today?
- Can the quality lead define acceptable stone variation and supply confirmed defect examples, and can a product-only camera operate at the current inspection point without obstructing staff?
- How many orders does Ankerstein handle weekly, what net time could extraction save after review, and how much weekly material-reporting time could realistically be removed after verification?
- How many stones are inspected weekly, and what evidence from rechecks, packing or complaints establishes the present escaped-visible-defect rate and a plausible reduction?

### Numbers to ask for

- Annual revenue and number of sets or stones sold
- Average realized selling price and gross margin by product
- Sales share and discounts by channel and destination market
- Material, labor, and packaging cost per saleable set
- Production capacity, utilization, and reject rate
- Relocation investment, remaining expenditure, and expected production downtime

### Gaps in the public research

- Homepage could not be read (ConnectError). Research relies on search only.
- No recent news found.

## 5. How these use cases were chosen

Every process step was rated against a rubric (money lever, HBR human role, opportunity type, full cost, feasibility, redesign-before-AI, augment vs substitute). The strongest steps were matched to a curated library via retrieval and company-fit reranking; three cards were adapted to support today's process. Deeper redesign appears only in section 3 (speculative Option B).

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

- Company record: [Spielwarenmesse - Spirit of Play | Building the future: with Ankersteinen for 140 years](https://www.spielwarenmesse.de/en/mag/toy-lab/building-the-future-with-ankersteinen-for-140-years)

## Appendix: Process details

Working hypothesis from public sources; validate the sequence, handoffs and systems with the company.
Evidence labels refer to the individual steps, not a verified end-to-end workflow.

| # | Step | What moves | Channel | Basis |
|---|------|------------|---------|-------|
| 1 | Order-handling staff turn incoming orders into production and delivery requirements | in: Requests or orders specifying products, quantities, and delivery destinations → out: Recorded orders and quantities needed for production or dispatch | Order records or spreadsheets (inferred; actual sales channel unknown) | *(assumption)* |
| 2 | Production staff arrange materials needed to make building stones | in: Required product quantities and available material stock → out: Material requirements and materials available for production | Spreadsheets or inventory records (inferred) | *(assumption)* |
| 3 | The Rudolstadt manufactory produces Anker building stones | in: Materials and instructions identifying the stones to be made → out: Manufactured building stones | Unknown; production records are not described | *([documented](https://www.spielwarenmesse.de/en/mag/toy-lab/building-the-future-with-ankersteinen-for-140-years))* |
| 4 | Production staff check stones and pack saleable products | in: Manufactured stones and required package contents → out: Checked, packed products and records of rejects or missing pieces | Manual checklists or spreadsheets (inferred) | *(assumption)* |
| 5 | Dispatch staff prepare outgoing orders for customers worldwide | in: Packed products, order quantities, and delivery addresses → out: Dispatched orders and shipment details | Shipping records or carrier booking tools (inferred) | *(assumption)* |

