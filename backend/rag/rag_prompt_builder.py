# backend/rag/rag_prompt_builder.py

def create_rag_prompt(query: str, context_chunks: list):
    """
    Build a clean prompt for RAG with proper citation support.
    """

    context_text = ""

    # Build context blocks with citation
    for c in context_chunks:
        source   = c.get("source", "unknown").upper()
        title    = c.get("title", "No Title")
        content  = c.get("content", "")
        citation = c.get("citation", title)

        context_text += (
            f"\n---\n"
            f"SOURCE: {source}\n"
            f"TITLE: {title}\n"
            f"CITATION: {citation}\n"
            f"CONTENT: {content}\n"
        )

    # Final prompt with instructions
    prompt = (
        "Use the following legal information to answer the user's question.\n\n"
        f"USER QUESTION:\n{query}\n\n"
        f"RELEVANT CONTEXT:\n{context_text}\n\n"
        "RULES:\n"
        "- Use only the given context — do not invent laws.\n"
        "- Always answer in 3 parts:\n"
        "  1. WHAT THE LAW SAYS: Explain the relevant law or section clearly.\n"
        "  2. WHAT SHE CAN DO: Give clear step-by-step actions she can take.\n"
        "  3. IMMEDIATE NEXT STEP: One specific action she should take right now.\n"
        "- Minimum 150 words for legal answers.\n"
        "- Use simple, clear language — avoid unnecessary legal jargon.\n"
        "- If information is missing from context, state that clearly.\n"
    )

    return prompt