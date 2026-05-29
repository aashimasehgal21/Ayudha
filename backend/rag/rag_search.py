# backend/rag/rag_search.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.db.supabase_client import get_supabase_client

load_dotenv()

client = OpenAI()
EMBED_MODEL = "text-embedding-3-small"


def get_embedding(text: str):
    """Generate embedding using OpenAI."""
    #Same embedding space as stored docs
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding



def add_citation(row, default_source):
    """
    Ensures every row has a 'citation' field.
    """
    title = row.get("title", "Unknown Title")
    source = row.get("source", default_source)

   
    citation = f"{source.upper()} → {title}"

    row["citation"] = citation
    return row




def search_laws(query: str, k: int):
    supabase = get_supabase_client()
    emb = get_embedding(query)

    response = supabase.rpc(
        "match_laws",
        {
            "query_embedding": emb,
            "match_count": k
        }
    ).execute()

    rows = response.data or []
    return [add_citation(r, "LAW") for r in rows]


def search_procedures(query: str, k: int):
    supabase = get_supabase_client()
    emb = get_embedding(query)

    response = supabase.rpc(
        "match_procedures",
        {
            "query_embedding": emb,
            "match_count": k
        }
    ).execute()

    rows = response.data or []
    return [add_citation(r, "PROCEDURE") for r in rows]


def search_templates(query: str, k: int):
    supabase = get_supabase_client()
    emb = get_embedding(query)

    response = supabase.rpc(
        "match_templates",
        {
            "query_embedding": emb,
            "match_count": k
        }
    ).execute()

    rows = response.data or []
    return [add_citation(r, "TEMPLATE") for r in rows]




def retrieve(query: str, total_k=6):
    """
    Retrieve laws, procedures, and templates evenly.
    """
    per_group = total_k // 3

    laws = search_laws(query, per_group)
    procedures = search_procedures(query, per_group)
    templates = search_templates(query, per_group)

    return laws + procedures + templates


# backend/rag/rag_search.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from backend.db.supabase_client import get_supabase_client

load_dotenv()
client = OpenAI()

EMBED_MODEL = "text-embedding-3-small"

def get_embedding(text: str):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=text
    )
    return response.data[0].embedding

def add_citation(row, default_source):
    title    = row.get("title", "Unknown Title")
    source   = row.get("source", default_source)
    citation = f"{source.upper()} → {title}"
    row["citation"] = citation
    return row

def search_laws(query: str, k: int):
    supabase = get_supabase_client()
    emb = get_embedding(query)
    response = supabase.rpc(
        "match_laws",
        {"query_embedding": emb, "match_count": k}
    ).execute()
    rows = response.data or []
    return [add_citation(r, "LAW") for r in rows]

def search_procedures(query: str, k: int):
    supabase = get_supabase_client()
    emb = get_embedding(query)
    response = supabase.rpc(
        "match_procedures",
        {"query_embedding": emb, "match_count": k}
    ).execute()
    rows = response.data or []
    return [add_citation(r, "PROCEDURE") for r in rows]

def search_templates(query: str, k: int):
    supabase = get_supabase_client()
    emb = get_embedding(query)
    response = supabase.rpc(
        "match_templates",
        {"query_embedding": emb, "match_count": k}
    ).execute()
    rows = response.data or []
    return [add_citation(r, "TEMPLATE") for r in rows]


# ─────────────────────────────────────────
# RE-RANKER
# ─────────────────────────────────────────
def rerank(query: str, chunks: list, top_k: int = 4) -> list:
    """
    Score each chunk by relevance to query.
    Uses keyword overlap + embedding similarity scoring.
    Returns top_k most relevant chunks only.
    """
    if not chunks:
        return []

    query_words = set(query.lower().split())

    # Remove stop words
    stop_words = {
        "what", "is", "the", "a", "an", "in", "of", "to",
        "how", "do", "i", "my", "me", "can", "for", "and",
        "or", "are", "was", "were", "be", "been", "will",
        "mujhe", "kya", "hai", "ka", "ki", "ke", "se", "mein"
    }
    query_words = query_words - stop_words

    scored = []
    for chunk in chunks:
        content = chunk.get("content", "").lower()
        title   = chunk.get("title", "").lower()

        # Keyword overlap score
        content_words = set(content.split())
        title_words   = set(title.split())

        kw_score = (
            len(query_words & content_words) * 1.0 +
            len(query_words & title_words)   * 2.0  # title match = higher weight
        )

        # Length penalty — very short chunks are usually less useful
        length_score = min(len(content) / 500, 1.0)

        # Source bonus — laws get slight priority for legal queries
        source = chunk.get("source", chunk.get("citation", "")).upper()
        source_bonus = 0.5 if "LAW" in source else 0.0

        total_score = kw_score + length_score + source_bonus

        scored.append((total_score, chunk))

    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)

    top = [chunk for _, chunk in scored[:top_k]]
    print(f"[Reranker] {len(chunks)} chunks → top {len(top)} selected")

    return top


# ─────────────────────────────────────────
# MAIN RETRIEVE — with re-ranker
# ─────────────────────────────────────────
def retrieve(query: str, total_k: int = 9) -> list:
    """
    Retrieve from all 3 tables, then re-rank to best 4.
    """
    per_group = total_k // 3

    laws       = search_laws(query, per_group)
    procedures = search_procedures(query, per_group)
    templates  = search_templates(query, per_group)

    all_chunks = laws + procedures + templates

    # Re-rank and return only best 4
    return rerank(query, all_chunks, top_k=4)