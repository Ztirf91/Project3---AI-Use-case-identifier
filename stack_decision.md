# Stack decision: LangGraph over n8n

**Choice:** LangGraph in Python is the primary stack. n8n is not a runtime here. Its public AI workflow templates are a source for the use-case library.

## Why LangGraph

1. **The product is judgment over shared state, not a chain of integrations.** Every step reads and extends one typed `RunState`: research, a business model with evidence, step ratings, retrieved cards, three picks. In LangGraph that state is a Pydantic model, so each node's output is validated, and the full state is saved as `state.json` next to every report.
2. **Rules are enforced in code, not left to the prompt.** Claims without a valid source id are downgraded to "assumption" in Python. The three picks are checked for distinct process steps, a quick win, a redesign case, and source cards that were actually retrieved, with one corrective retry. That is a few lines of Python. It would be a tangle of IF and Code nodes in n8n.
3. **Structured output and RAG are first-class.** `with_structured_output()` returns typed objects, and the Pinecone retrieval is an ordinary function call inside a node.
4. **Failure stays partial.** A blocked website, an empty search, or a failed model call is written into the state as a note, and the graph still renders a report that lists the gap as a question for the meeting.
5. **A grader can run it.** One repository, `pip install -r requirements.txt`, three API keys, one command. No n8n instance, credentials store, or workflow import needed.

## What n8n would have done better

A visual canvas for a non-technical audience, ready-made connectors to CRMs and email, and a hosted webhook trigger. These matter for the go-to-market sprints (a lead form that triggers a report). The graph can later sit behind an n8n or simple webhook front end without changing the core.

## Supporting choices

| Part | Choice | Reason |
|---|---|---|
| Model | `gpt-4o-mini` | Cheap, reliable structured output; about 4 calls per report |
| Search | Tavily | Built for agents, returns clean snippets and URLs, free tier covers the project |
| Vector store | Pinecone (serverless) | Managed, free starter tier, the use-case library can grow without code changes |
| Embeddings | OpenAI `text-embedding-3-small` | Same provider as the model, 1536 dimensions |
| Website reading | `httpx` and BeautifulSoup | Free, no crawler API; careers pages are followed two levels deep to reach real postings |
| Report | Jinja2 template | Same structure every time, no extra model call |
