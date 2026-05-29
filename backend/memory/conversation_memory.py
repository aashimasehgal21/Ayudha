# backend/memory/conversation_memory.py
# backend/memory/conversation_memory.py

import os
from dotenv import load_dotenv

load_dotenv()

try:
    from langchain_community.chat_message_histories import PostgresChatMessageHistory

    SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

    if not SUPABASE_DB_URL:
        raise Exception("SUPABASE_DB_URL not set, using in-memory")

    def get_session_history(session_id: str):
        return PostgresChatMessageHistory(
            connection_string=SUPABASE_DB_URL,
            session_id=session_id
        )

    print("[Memory] Using persistent Postgres memory")

except Exception as e:
    print(f"[Memory] Falling back to in-memory: {e}")
    from langchain_community.chat_message_histories import ChatMessageHistory

    _store = {}

    def get_session_history(session_id: str):
        if session_id not in _store:
            _store[session_id] = ChatMessageHistory()
        return _store[session_id]