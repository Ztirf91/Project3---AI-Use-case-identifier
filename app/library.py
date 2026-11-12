"""Use-case library: YAML cards embedded in a local Chroma collection."""

import os
import sys

import chromadb
import yaml
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from app.config import CHROMA_DIR, COLLECTION, EMBEDDING_MODEL, USE_CASES_DIR

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
        ]
    )


def _collection(client: chromadb.ClientAPI):
    embed = OpenAIEmbeddingFunction(api_key=os.environ["OPENAI_API_KEY"], model_name=EMBEDDING_MODEL)
    return client.get_or_create_collection(COLLECTION, embedding_function=embed, metadata={"hnsw:space": "cosine"})


def build_index() -> int:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if COLLECTION in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION)
    cards = load_cards()
    _collection(client).add(
        ids=[c["id"] for c in cards],
        documents=[card_text(c) for c in cards],
        metadatas=[{"title": c["title"], "file": c["file"]} for c in cards],
    )
    return len(cards)


def search(query: str, n: int = 3) -> list[dict]:
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    result = _collection(client).query(query_texts=[query], n_results=n)
    by_id = {c["id"]: c for c in load_cards()}
    hits = []
    for card_id, distance in zip(result["ids"][0], result["distances"][0]):
        if card_id in by_id:
            hits.append({**by_id[card_id], "similarity": round(1 - distance, 3)})
    return hits


if __name__ == "__main__":
    print(f"Indexed {build_index()} use-case cards into {CHROMA_DIR}")
