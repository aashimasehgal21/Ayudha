# backend/agent/agent_core.py

from typing import Optional
from backend.agent.classifier import classify_query
from backend.agent.agent_prompts import ANSWER_PROMPT_GENERAL

# Load RAG pipeline
try:
    from backend.rag.test_rag import run_rag_pipeline
except Exception:
    run_rag_pipeline = None


# -------------------------------
# Optional MCP tools
# -------------------------------
def _import_mcp_tool(module, class_name):
    try:
        m = __import__(module, fromlist=[class_name])
        return getattr(m, class_name)()
    except Exception:
        return None


date_normalizer = _import_mcp_tool("backend.mcp.date_normalizer", "DateNormalizer")
calculator = _import_mcp_tool("backend.mcp.calculator", "Calculator")


# -------------------------------
# OpenAI Client (Correct API)
# -------------------------------
try:
    from openai import OpenAI
    _client = OpenAI()
except Exception:
    _client = None


# -----------------------------------------
# FIXED LLM CALL — correct content extraction
# -----------------------------------------
def _llm_answer(query: str) -> str:
    """
    Uses the correct OpenAI ChatCompletion API.
    """
    if _client is None:
        return "LLM not configured."

    prompt = ANSWER_PROMPT_GENERAL.format(query=query)

    try:
        response = _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        # ✔ FIX: ChatCompletionMessage uses DOT notation
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"LLM error: {e}"


# -------------------------------
# Tools activation check
# -------------------------------
def _uses_date_tool(q: str) -> bool:
    q = q.lower()
    return any(k in q for k in ["today", "tomorrow", "yesterday", "next", "last", "date", "ago"])


def _uses_calc_tool(q: str) -> bool:
    q = q.lower()
    if any(word in q for word in ["age", "years", "months", "calculate", "difference"]):
        return True
    return any(ch.isdigit() for ch in q)


# -------------------------------
# MASTER AGENT ROUTER
# -------------------------------
def agent_answer(user_query: str) -> str:
    """
    Decides whether to call RAG, tools, or general LLM.
    """

    # 1. Classify
    category = classify_query(user_query)
    print(f"[Agent] Category: {category}")

    # 2. Run tools
    tool_outputs = []

    if _uses_date_tool(user_query) and date_normalizer:
        try:
            tool_outputs.append(("date_normalizer", date_normalizer.run(text=user_query)))
        except Exception as e:
            tool_outputs.append(("date_normalizer_error", str(e)))

    if _uses_calc_tool(user_query) and calculator:
        try:
            tool_outputs.append(("calculator", calculator.run(text=user_query)))
        except Exception as e:
            tool_outputs.append(("calculator_error", str(e)))

    # 3. RAG Pipeline for legal queries
    if category in ("LAW", "PROCEDURE", "TEMPLATE") and run_rag_pipeline:

        try:
            rag_ans = run_rag_pipeline(user_query)

            if isinstance(rag_ans, dict) and "answer" in rag_ans:
                return rag_ans["answer"]

            if isinstance(rag_ans, str):
                return rag_ans

            return str(rag_ans)

        except Exception as e:
            print("RAG error:", e)
            return _llm_answer(user_query)

    # 4. General LLM with appended tool results
    if tool_outputs:
        extra = "\n\nTOOL OUTPUTS:\n" + "\n".join(f"{k}: {v}" for k, v in tool_outputs)
        user_query = user_query + extra

    return _llm_answer(user_query)




