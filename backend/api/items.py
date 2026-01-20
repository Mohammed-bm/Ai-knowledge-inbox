from fastapi import APIRouter
from typing import List

from db import cursor

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def list_items():
    """
    Returns all saved notes and URLs
    (no chunks, no embeddings)
    """

    cursor.execute("""
        SELECT
            id,
            type,
            source,
            raw_text,
            created_at
        FROM items
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()

    items = []

    for item_id, item_type, source, raw_text, created_at in rows:
        preview = raw_text[:100] + "..." if len(raw_text) > 100 else raw_text

        items.append({
            "id": item_id,
            "type": item_type,
            "source": source,
            "preview": preview,
            "created_at": created_at
        })

    return items
