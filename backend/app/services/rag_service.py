"""
NCTB RAG Service
পাঠ্যপুস্তক PDF থেকে প্রাসঙ্গিক তথ্য উদ্ধার করো
ChromaDB + Google Gemini Embedding ব্যবহার করে
"""

import chromadb
from google import genai
from app.core.config import settings
from typing import Optional

_chroma_client: Optional[chromadb.PersistentClient] = None
_collection = None
_genai_client: Optional[genai.Client] = None


def get_genai_client() -> genai.Client:
    global _genai_client
    if _genai_client is None:
        _genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
    return _genai_client


def get_collection():
    global _chroma_client, _collection
    if _collection is None:
        _chroma_client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        try:
            _collection = _chroma_client.get_collection(settings.CHROMA_COLLECTION)
        except Exception:
            _collection = _chroma_client.create_collection(settings.CHROMA_COLLECTION)
    return _collection


def get_query_embedding(query: str) -> list:
    client = get_genai_client()
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=[query],
    )
    return result.embeddings[0].values


async def retrieve_nctb_context(
    subject: str,
    chapter_id: str,
    query: str,
    k: int = 3
) -> str:
    try:
        collection = get_collection()
        search_query = f"{subject} {chapter_id} {query}"
        embedding = get_query_embedding(search_query)
        where_filter = {"subject": subject} if subject else None

        results = collection.query(
            query_embeddings=[embedding],
            n_results=k,
            where=where_filter,
        )

        if not results["documents"] or not results["documents"][0]:
            return "পাঠ্যপুস্তকে প্রাসঙ্গিক তথ্য পাওয়া যায়নি।"

        context_parts = []
        for i, (doc, meta) in enumerate(
            zip(results["documents"][0], results["metadatas"][0]), 1
        ):
            source = meta.get("source", "NCTB")
            page   = meta.get("page", "")
            context_parts.append(f"[{i}] {doc} (উৎস: {source}, পৃষ্ঠা: {page})")

        return "\n\n".join(context_parts)

    except Exception as e:
        print(f"RAG retrieval error: {e}")
        return "পাঠ্যপুস্তক থেকে তথ্য লোড করা যাচ্ছে না।"
