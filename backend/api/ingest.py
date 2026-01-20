from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
import json
from db import conn, cursor
from utils import clean_text, chunk_text, EmbeddingService, fetch_and_clean_url

router = APIRouter(prefix="/ingest", tags=["ingest"])

embedding_service = EmbeddingService()

class IngestRequest(BaseModel):
    type: str              # "note" | "url"
    raw_text: Optional[str] = None
    source: Optional[str] = None

@router.post("/")
def ingest_item(data: IngestRequest):

    if data.type not in ["note", "url"]:
        raise HTTPException(status_code=400, detail="Invalid type")

    if data.type == "note":
        if not data.raw_text or not data.raw_text.strip():
            raise HTTPException(status_code=400, detail="raw_text is required for notes")
        text = data.raw_text
        source = None

    elif data.type == "url":
        if not data.source or not data.source.strip():
            raise HTTPException(status_code=400, detail="source URL is required")

        text = fetch_and_clean_url(data.source)
        source = data.source

    try:
        item_id = str(uuid.uuid4())

        cursor.execute(
            """
            INSERT INTO items (id, type, source, raw_text)
            VALUES (?, ?, ?, ?)
            """,
            (item_id, data.type, source, text),
        )

        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text)

        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks created")

        embeddings = embedding_service.embed_texts(chunks)

        for chunk_text_value, embedding in zip(chunks, embeddings):
            cursor.execute(
                """
                INSERT INTO chunks (chunk_id, item_id, chunk_text, embedding)
                VALUES (?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    item_id,
                    chunk_text_value,
                    json.dumps(embedding),
                ),
            )

        conn.commit()

        return {
            "status": "success",
            "item_id": item_id,
            "chunks_stored": len(chunks),
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
