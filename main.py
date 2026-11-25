
import io
import time
from functools import lru_cache
from typing import List, Dict, Tuple

import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# PDF chunking and retrieval
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
TOP_K = 4

# Try the primary model first, then a lighter fallback.
GEMINI_MODELS = [
    "gemini-3.8-flash",
    "gemini-3.5-flash-lite",
]


def extract_pdf_pages(pdf_bytes: bytes) -> List[Dict]:
    """Extract selectable text from each PDF page."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text,
            })

    if not pages:
        raise ValueError(
            "No selectable text found in the PDF. "
            "If it is scanned, run OCR first."
        )

    return pages


def split_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> List[str]:
    """Split text into overlapping chunks."""
    text = " ".join(text.split())

    if not text:
        return []

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "Invalid chunk settings: overlap must be smaller "
            "than chunk_size."
        )

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - overlap

    return chunks


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the embedding model once per process."""
    return SentenceTransformer(EMBEDDING_MODEL)


def build_vector_store(pdf_bytes: bytes) -> Dict:
    """Create a FAISS index from PDF text chunks."""
    pages = extract_pdf_pages(pdf_bytes)
    chunks = []

    for page in pages:
        for chunk in split_text(page["text"]):
            chunks.append({
                "page": page["page"],
                "text": chunk,
            })

    if not chunks:
        raise ValueError("The PDF did not contain text to index.")

    model = get_embedding_model()

    vectors = model.encode(
        [item["text"] for item in chunks],
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    ).astype("float32")

    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    return {
        "index": index,
        "chunks": chunks,
        "model": model,
    }


def retrieve(
    question: str,
    vector_store: Dict,
    top_k: int = TOP_K,
) -> List[Dict]:
    """Retrieve the most relevant PDF chunks."""
    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    if not vector_store["chunks"]:
        return []

    query_vector = vector_store["model"].encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True,
    ).astype("float32")

    number_to_search = min(top_k, len(vector_store["chunks"]))

    scores, indices = vector_store["index"].search(
        query_vector,
        number_to_search,
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0:
            item = dict(vector_store["chunks"][int(idx)])
            item["score"] = float(score)
            results.append(item)

    return results


def _generate_with_retry(client, model_name: str, prompt: str):
    """Retry temporary Gemini errors with exponential backoff."""
    from google.genai.errors import APIError

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            answer = getattr(response, "text", None)

            if answer and answer.strip():
                return answer.strip()

            raise RuntimeError(
                f"Gemini model {model_name} returned an empty response."
            )

        except APIError as exc:
            code = getattr(exc, "code", None)

            if code not in (429, 500, 502, 503, 504):
                raise

            if attempt == max_attempts - 1:
                raise

            # Wait 2, then 4 seconds before retrying.
            time.sleep(2 ** (attempt + 1))

    raise RuntimeError("Gemini could not generate an answer.")


def answer_question(
    question: str,
    vector_store: Dict,
    api_key: str,
) -> Tuple[str, List[Dict]]:
    """Answer a question using retrieved PDF passages only."""
    from google import genai
    from google.genai.errors import APIError

    question = question.strip()

    if not question:
        raise ValueError("Please enter a question.")

    if not api_key or not api_key.strip():
        raise ValueError("Please enter your Gemini API key in Settings.")

    sources = retrieve(question, vector_store)

    if not sources:
        return (
            "I couldn't find that information in the uploaded PDF.",
            [],
        )

    context = "\n\n".join(
        f"[Page {item['page']}]\n{item['text']}"
        for item in sources
    )

    prompt = f"""You are a careful PDF question-answering assistant.

Rules:
- Answer using ONLY the supplied PDF excerpts.
- If the excerpts do not contain the answer, say:
  "I couldn't find that information in the uploaded PDF."
- Do not invent facts or use outside knowledge.
- Be clear and concise.
- Cite relevant page numbers, for example (Page 2).

PDF EXCERPTS:
{context}

USER QUESTION:
{question}

ANSWER:
"""

    client = genai.Client(api_key=api_key.strip())
    last_error = None

    for model_name in GEMINI_MODELS:
        try:
            answer = _generate_with_retry(
                client,
                model_name,
                prompt,
            )
            return answer, sources

        except APIError as exc:
            code = getattr(exc, "code", None)

            # Try the next model only for temporary service errors
            # or rate limits. Do not hide authentication/model errors.
            if code not in (429, 500, 502, 503, 504):
                raise

            last_error = exc

        except RuntimeError as exc:
            # Empty model responses are also eligible for fallback.
            last_error = exc

    raise RuntimeError(
        "All configured Gemini models failed. "
        "Please try again later. Last error: "
        f"{last_error}"
    )
