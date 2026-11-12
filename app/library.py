"""Use-case library: YAML cards embedded with OpenAI and stored in a Pinecone index."""

import os
import sys
import time

import yaml
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec

from app.config import EMBEDDING_DIMENSION, EMBEDDING_MODEL, PINECONE_INDEX, PINECONE_NAMESPACE, USE_CASES_DIR

REQUIRED = ("id", "title", "source_url", "pattern", "ai_does")


def load_cards() -> list[dict]:
    cards = []
    for path in sorted(USE_CASES_DIR.glob("*.y*ml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or []
        for card in data if isinstance(data, list) else [data]:
            missing = [f for f in REQUIRED if not card.get(f)]
            if missing:
                print(f"Skipping card in {path.name}: missing {missing}", file=sys.stderr)
                continue
            card["file"] = path.name
            cards.append(card)
    ids = [c["id"] for c in cards]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        raise ValueError(f"Duplicate card ids: {sorted(duplicates)}")
    return cards


def card_text(card: dict) -> str:
    return "\n".join(
        [
            card["title"],
            f"Pattern: {card['pattern']}",
            f"AI does: {card['ai_does']}",
            f"Process types: {', '.join(card.get('process_types', []))}",
            f"Needs: {', '.join(card.get('needs', []))}",
            f"Task scope: {card.get('task_scope', '')}",
        ]
    )


def _embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


def _index(create: bool = False):
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    if not pc.has_index(PINECONE_INDEX):
        if not create:
            raise RuntimeError(f"Pinecone index '{PINECONE_INDEX}' not found. Run: python -m app.library")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(PINECONE_INDEX)


def build_index() -> int:
    cards = load_cards()
    index = _index(create=True)
    if PINECONE_NAMESPACE in (index.describe_index_stats().namespaces or {}):
        index.delete(delete_all=True, namespace=PINECONE_NAMESPACE)

    vectors = _embeddings().embed_documents([card_text(c) for c in cards])
    index.upsert(
        vectors=[
            {"id": c["id"], "values": v, "metadata": {"title": c["title"], "file": c["file"]}}
            for c, v in zip(cards, vectors)
        ],
        namespace=PINECONE_NAMESPACE,
    )

    for _ in range(30):
        namespace = (index.describe_index_stats().namespaces or {}).get(PINECONE_NAMESPACE)
        if namespace and namespace.vector_count == len(cards):
            break
        time.sleep(1)
    return len(cards)


def search(query: str, n: int = 3) -> list[dict]:
    vector = _embeddings().embed_query(query)
    result = _index().query(vector=vector, top_k=n, namespace=PINECONE_NAMESPACE)
    by_id = {c["id"]: c for c in load_cards()}
    return [{**by_id[m.id], "similarity": round(m.score, 3)} for m in result.matches if m.id in by_id]


if __name__ == "__main__":
    count = build_index()
    print(f"Indexed {count} use-case cards into Pinecone index '{PINECONE_INDEX}' (namespace '{PINECONE_NAMESPACE}')")
