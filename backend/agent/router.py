# backend/agent/router.py

from fastapi import APIRouter
from pydantic import BaseModel

# 👉 NEW: LangChain-based agent
from backend.agent.agent_langchain import AyudhaAgentExecutor

router = APIRouter()

# Create agent instance (once)
agent = AyudhaAgentExecutor()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint using Agentic Layer (LangChain).
    The agent decides whether to use RAG or answer directly.
    let the agentic layer decide whether to use RAG or direct LLM response
    general answer should be preferred first and legal answer should be given only when asked specifically 
    or when the user is asking for anything related to law, legal procedures, legal rights, legal acts, sections, templates or notices.
    or the user is unsure about legal matters.
    """
    try:
        answer = agent.answer(request.query)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}


