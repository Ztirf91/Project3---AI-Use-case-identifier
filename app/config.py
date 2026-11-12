import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

MODEL = os.getenv("MODEL", "gpt-4o-mini")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "ai-use-cases")
PINECONE_NAMESPACE = "use-cases"
CORPUS_DIR = ROOT / "corpus"
RUBRIC_PATH = CORPUS_DIR / "frameworks" / "rubric.md"
USE_CASES_DIR = CORPUS_DIR / "use_cases"
OUTPUTS_DIR = ROOT / "outputs"


def llm(temperature: float = 0.2) -> ChatOpenAI:
    return ChatOpenAI(model=MODEL, temperature=temperature, max_retries=3, timeout=120)
