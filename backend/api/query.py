from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import json
import numpy as np

from db import cursor
from utils import clean_text, EmbeddingService, llm_service

router = APIRouter(prefix="/query", tags=["query"])

embedding_service = EmbeddingService()

class QueryRequest(BaseModel):
    question: str
    top_k: int = 3

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Cosine similarity for normalized vectors
    """
    return float(np.dot(a, b))

@router.post("")
def query_knowledge(data: QueryRequest):
    if not data.question.strip():
        raise HTTPException(status_code=400, detail="Question is empty")

    # 1️⃣ Clean + embed query
    query_text = clean_text(data.question)
    query_embedding = np.array(
        embedding_service.embed_query(query_text)
    )

    # 2️⃣ Load all chunks
    cursor.execute("""
        SELECT
            chunks.chunk_text,
            chunks.embedding,
            items.type,
            items.source
        FROM chunks
        JOIN items ON chunks.item_id = items.id
    """)

    rows = cursor.fetchall()

    if not rows:
        return {
            "answer": "No data available.",
            "sources": []
        }

    results = []

    # 3️⃣ Compute similarity
    for chunk_text, embedding_json, item_type, source in rows:
        chunk_embedding = np.array(json.loads(embedding_json))
        score = cosine_similarity(query_embedding, chunk_embedding)

        results.append({
            "score": score,
            "text": chunk_text,
            "type": item_type,
            "source": source
        })

    # 4️⃣ Sort + select top K
    results.sort(key=lambda x: x["score"], reverse=True)
    top_results = results[: data.top_k]

    context = "\n\n".join([r["text"] for r in top_results])

    answer = llm_service.generate_answer(
        question=data.question,
        context=context
    )


    # 6️⃣ Return answer + sources
    return {
        "answer": answer,
        "sources": [
            {
                "snippet": r["text"],
                "source": r["source"],
                "type": r["type"],
                "score": round(r["score"], 4)
            }
            for r in top_results
        ]
    }
    