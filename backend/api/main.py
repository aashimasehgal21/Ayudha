# backend/api/main.py

import os
import uuid
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from backend.agent.agent_langchain import AyudhaAgentExecutor

app = FastAPI(title="Ayudha - Women's Legal Assistant")

agent = AyudhaAgentExecutor()

class ChatRequest(BaseModel):
    query: str
    session_id: str = ""

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        session_id = req.session_id if req.session_id else str(uuid.uuid4())
        answer = agent.answer(req.query)
        return {
            "answer": answer,
            "session_id": session_id
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "answer": "Something went wrong. Please try again."
            }
        )

@app.get("/health")
async def health():
    return {"status": "ok", "service": "Ayudha"}