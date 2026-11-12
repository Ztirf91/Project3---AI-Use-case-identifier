# How to think about AI in a company: the rubric

Short notes in our own words. Each section ends with the check question the agent applies to every process step, and the public source it is based on. The original articles are not reproduced here.

## 1. Start from the money, not from the technology

A use case only matters if it moves how the company earns money: more units sold, a better price, a lower cost per unit, or less risk on each unit. Teams often waste effort on areas of marginal value. Begin with the processes that are costly or central to the business, then ask whether AI could make them faster, cheaper, or more precise.

Check: Which lever of the unit economics does this step touch, and how much of the business runs through it?

Sources: appliedAI, *How to find and prioritize AI use cases* (2020), https://www.appliedai.de/uploads/files/Whitepapers/appliedAI-Whitepaper-Applying-AI-How-to-find-and-prioritize-AI-use-cases-2020-EN.pdf

## 2. Automate tasks, not jobs

Jobs and departments are bundles of tasks. Some tasks are easy for a language model, others are not. Break each process into concrete tasks with a clear input and output before judging it. "Sales" is not a use case. "Turn an emailed dealer request into a draft quote" is.

Check: Is this a concrete task with a defined input and output?

Sources: MIT Sloan, *How to find the right business use cases for generative AI* (2025), https://mitsloan.mit.edu/ideas-made-to-matter/how-to-find-right-business-use-cases-generative-ai ; appliedAI (2020), link above

## 3. Error cost and type of knowledge decide the human's role

Two questions decide how much AI can do alone. What does a mistake cost: a small inefficiency, or legal, financial, or reputational damage? And is the needed knowledge explicit (documents, data, rules) or tacit (experience, judgment, relationships)?

- Low error cost, explicit knowledge: **No regrets**. AI can run the task end to end.
- Low error cost, tacit knowledge: **Creative catalyst**. AI produces options, a person chooses.
- High error cost, explicit knowledge: **Quality control**. AI produces, a person verifies.
- High error cost, tacit knowledge: **Human first**. A person leads, AI assists with parts.

Check: What does an error here cost, and is the knowledge written down or in people's heads?

Source: Anand and Wu, *The Gen AI Playbook for Organizations*, Harvard Business Review (Nov 2025), https://hbr.org/2025/11/the-gen-ai-playbook-for-organizations and the framework visual https://hbr.org/data-visuals/2025/11/a-framework-for-choosing-where-and-how-to-use-gen-ai

## 4. Where AI helps first

Good first targets are repetitive low-value work, skill bottlenecks where people wait for an expert, and ambiguous tasks where people struggle to get started. Most real use cases are one of six basic types: content creation, research, coding, data analysis, ideation and strategy, and automation. Today, generative AI is strongest on structured tasks (a predictable order of steps) and processing tasks (interpreting, extracting, summarizing, or transforming existing information).

Check: Is this step repetitive, a bottleneck, or a blank page, and which primitive would do the work?

Sources: OpenAI, *Identifying and scaling AI use cases*, https://openai.com/business/learn/identifying-and-scaling-ai-use-cases/ ; Taylor Radey, *Finding AI use cases: one helpful framework to try* (2025), https://www.taylorradey.com/post/finding-ai-use-cases-framework

## 5. Count all the costs, then compare with today

The model fee is the smallest cost. The larger ones are making the output correct enough for the task, and building a way to catch and fix errors, often a person in the loop. Compare that full cost with the cost of doing the task as it is done today. If AI does not win, park the idea and revisit it later, since costs keep falling.

Check: Including review effort, is the AI version clearly cheaper or better than today's way?

Source: MIT Sloan (2025), link above

## 6. Feasibility: data, systems, know-how

Ease of implementation depends on four things. Is the data there, in usable quality, and kept up to date? Has someone already solved this, inside or outside the industry? How much do processes and systems have to change? Does the company have the know-how to run it? Prototypes are easy, scaling is hard, so maintenance and data updates belong in the estimate. Flag steps that touch personal data or sensitive decisions for a regulatory check.

Check: Does the data exist, is there a proven pattern, and what has to change in the systems?

Source: appliedAI (2020), link above

## 7. Fix the process before automating it

AI can support an existing process or replace it with a better one. Automating a poor process only makes the waste faster. Where a step is a workaround (re-typing, chasing information, duplicate checks), the better move is often to remove or redesign the step and then let AI handle what remains.

Check: Should this step exist in its current form, or should it be redesigned first?

Sources: appliedAI (2020), link above ; HBR (2025), link above

## 8. Prioritize: quick wins first, but not only

Plot use cases by value and effort. Start with high-value, low-effort quick wins to build momentum and learning. For companies new to AI, the first case should have available data and a proven pattern elsewhere, and be visible in the core business. Large, complex cases should be broken into smaller steps with value at each stage. Do low-stakes things first, but do several of them quickly.

Check: Is this a quick win, a redesign, or a strategic bet, and is there a smaller first step?

Sources: OpenAI, link above ; appliedAI (2020), link above ; MIT Sloan (2025), link above

## 9. People stay in the sandwich

In most knowledge work the person sets up the task, the AI executes it, and the person reviews and completes it. The role shifts from doing the task to directing and checking it. Use cases should say who owns the review.

Check: Who sets the task up, and who signs off the result?

Source: Taylor Radey (2025), link above

## 10. Prove value in a focused pilot before scaling

Start with a business problem and map the affected workflow with its owner and users. Record today's performance, the desired outcome, and a success measure before proposing AI. Compare candidates consistently on value, process and data readiness, governance, workforce impact, and time to measurable results. A working prototype alone does not justify scaling: a focused pilot must show reliable output, useful performance gains, workable handoffs, and user adoption. Name the accountable owner and the conditions for broader rollout.

Check: What baseline and success measure will the pilot use, who owns it, and what evidence would justify scaling?

Source: APQC, *How Can Organizations Identify And Prioritize Valuable AI Use Cases?*, https://www.apqc.org/How-Can-Organizations-Identify-And-Prioritize-Valuable-AI-Use-Cases

## 11. Define when, what, who, and how for agentic work

For an agentic use case, separate the trigger and task from the actor and its capabilities. Work can begin with a human request, delegation, a schedule, or an external event. In AWS's taxonomy, an agent carries instructions, capabilities, and learned context; tools perform individual operations, skills provide reusable guidance with room for judgment, and workflows fix coordination and control flow in code. Choose the simplest arrangement that meets the required consistency and oversight. A recurring task may only need a new trigger for an existing agent. Use deterministic workflows where fixed ordering, error handling, and auditability matter.

Check: What starts this task, what must it achieve, who performs it, and which tools, guidance, or fixed workflow provide the required control?

Source: AWS, Thomas Delteil, Adi Kalyanpur, and Ron Litman, *Taxonomy of agentic primitives in Amazon Quick* (6 November 2026), https://aws.amazon.com/blogs/machine-learning/taxonomy-of-agentic-primitives-in-amazon-quick/
