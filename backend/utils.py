from sentence_transformers import SentenceTransformer
from typing import List
from bs4 import BeautifulSoup
import re
import requests
import hashlib
import os
from typing import Optional
from google import genai
from dotenv import load_dotenv

load_dotenv()

def clean_text(text: str) -> str:
    """
    Basic text cleaning before chunking / embedding
    """
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def chunk_text(
    text: str,
    chunk_size: int = 200,
    overlap: int = 40
) -> List[str]:
    """
    Splits text into overlapping chunks
    """
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

        if start < 0:
            start = 0

    return chunks

def fetch_and_clean_url(url: str) -> str:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove junk
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        # Extract visible text
        texts = [
            p.get_text(separator=" ", strip=True)
            for p in soup.find_all("p")
        ]

        text = " ".join(texts)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    except Exception as e:
        print("URL extraction error:", e)
        return ""

# utils.py (or services/llm.py)
class LLMService:
    def __init__(self):
        self.client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    def generate_answer(self, question: str, context: Optional[str] = None) -> str:
        if context:
            prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the provided context.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
"""
        else:
            prompt = question

        response = self.client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt,
        )

        return response.text.strip()


# Singleton instance
llm_service = LLMService()

# ----------------------------
# Embedding Service
# ----------------------------

class EmbeddingService:
    """
    Local embedding service using SentenceTransformers
    """

    def __init__(self):
        # Loads once when FastAPI starts
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Embed multiple texts (for ingestion)
        """
        embeddings = self.model.encode(
            texts,
            batch_size=32,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query (for search)
        """
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embedding.tolist()
