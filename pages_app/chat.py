# pages_app/chat.py

import streamlit as st
import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND = "http://127.0.0.1:8000"


def clean_answer(text: str) -> str:
    text = re.sub(r'\*?\*?SOURCE[S]?\*?\*?\s*[→-]?\s*TITLE\s*entries?\s*used:?.*',
                  '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\*?\*?SOURCE[S]?\*?\*?:.*', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'\*?\*?Sources?\s*Used\*?\*?:.*', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'(LAW|TEMPLATE|PROCEDURE)\s*[→-].*', '', text, flags=re.MULTILINE)
    return text.strip()


def show():
    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Home"
            st.rerun()
    with col_title:
        st.markdown("""
        <div style='font-family:Playfair Display,serif;font-size:24px;
        font-weight:700;color:#1a1a1a;padding-top:4px'>💬 Legal Chat</div>
        """, unsafe_allow_html=True)

    st.caption("Ask any legal question — get guidance on laws, rights & IPC sections")
    st.divider()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = ""
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None

    # Chat display
    if not st.session_state.chat_history and not st.session_state.pending_query:
        st.markdown("""
        <div style='text-align:center;padding:40px 20px'>
            <div style='font-size:52px;margin-bottom:14px'>⚖️</div>
            <div style='font-size:17px;font-weight:700;color:#1a1a1a'>
            How can I help you today?</div>
            <div style='font-size:13px;margin-top:8px;color:#888'>
            Ask about laws, your rights, FIR process, or any legal matter</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='display:flex;justify-content:flex-end;margin:10px 0'>
                <div style='background:#b5354a;color:#ffffff;padding:13px 18px;
                border-radius:20px 20px 4px 20px;max-width:70%;font-size:15px;
                line-height:1.5;font-weight:500;
                box-shadow:0 2px 8px rgba(181,53,74,0.25)'>
                {msg["content"]}</div></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display:flex;justify-content:flex-start;margin:10px 0'>
                <div style='background:#ffffff;color:#1a1a1a;padding:14px 20px;
                border-radius:20px 20px 20px 4px;max-width:74%;font-size:15px;
                line-height:1.7;border:1.5px solid #f5c6ce;
                box-shadow:0 2px 8px rgba(181,53,74,0.08)'>
                {msg["content"]}</div></div>
                """, unsafe_allow_html=True)

    # Process pending query BEFORE showing input
    if st.session_state.pending_query:
        query = st.session_state.pending_query
        st.session_state.pending_query = None

        # Show spinner right after chat history
        with st.spinner("⏳ Ayudha is answering..."):
            try:
                res = requests.post(
                    f"{BACKEND}/chat",
                    json={"query": query,
                          "session_id": st.session_state.session_id},
                    timeout=30
                )
                data = res.json()
                raw_answer = data.get("answer", "Something went wrong.")
                answer = clean_answer(raw_answer)
                st.session_state.session_id = data.get("session_id", "")
            except Exception as e:
                answer = (
                    f"⚠️ Cannot connect to backend. "
                    f"Make sure FastAPI is running.\n\nError: {e}"
                )
        st.session_state.chat_history.append({
            "role": "bot", "content": answer
        })
        st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Input form
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([7, 1])
        with col1:
            user_input = st.text_input(
                "msg", placeholder="Type your question here...",
                label_visibility="collapsed"
            )
        with col2:
            send = st.form_submit_button("Send →")

    # Quick questions
    st.markdown(
        "<div style='font-size:13px;font-weight:600;color:#1a1a1a;"
        "margin:10px 0 8px'>Quick questions:</div>",
        unsafe_allow_html=True
    )
    suggestions = [
        "What is IPC Section 498A?", "How to file an FIR?",
        "What is the POSH Act?", "Rights under domestic violence act",
        "What is IPC 354?", "How to get a protection order?"
    ]
    q_cols = st.columns(3)
    for i, q in enumerate(suggestions):
        with q_cols[i % 3]:
            if st.button(q, key=f"sq_{i}", use_container_width=True):
                user_input = q
                send = True

    if send and user_input and user_input.strip():
        st.session_state.chat_history.append({
            "role": "user", "content": user_input
        })
        st.session_state.pending_query = user_input
        st.rerun()

    if st.session_state.chat_history:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.session_id = ""
            st.session_state.pending_query = None
            st.rerun()