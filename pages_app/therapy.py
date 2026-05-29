# pages_app/therapy.py

import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

THERAPY_SYSTEM = """
You are a warm, empathetic emotional support companion for women going through difficult times.
Do NOT give legal advice here. Just listen, validate feelings, and offer gentle support.
Respond in simple English. Keep responses short, warm, and supportive — 3-5 sentences max.
End each response with one calming suggestion or affirmation.
Ask in end do ypu want to talk about your feel, Am here to listen
"""


def show():
    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Home"
            st.rerun()
    with col_title:
        st.markdown("""
        <div style='font-family:Playfair Display,serif;font-size:24px;
        font-weight:700;color:#1a1a1a;padding-top:4px'>🧘 Emotional Support</div>
        """, unsafe_allow_html=True)

    st.caption("This is a safe space — talk freely, no judgment, just support")
    st.divider()

    st.markdown("""
    <div style='background:#fdf0f2;border:1px solid #f5c6ce;border-radius:10px;
    padding:12px 18px;font-size:13px;color:#b5354a;margin-bottom:16px'>
    💙 This space is just for you. Share whatever you feel — Ayudha is listening.
    </div>
    """, unsafe_allow_html=True)

    if "therapy_history" not in st.session_state:
        st.session_state.therapy_history = []

    # Chat display
    if not st.session_state.therapy_history:
        st.markdown("""
        <div style='text-align:center;padding:40px 20px'>
            <div style='font-size:52px;margin-bottom:12px'>🤗</div>
            <div style='font-size:16px;font-weight:600;color:#555'>
            How are you feeling today?</div>
            <div style='font-size:13px;margin-top:6px;color:#aaa'>
            You can share anything — I am here to listen</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.therapy_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div style='display:flex;justify-content:flex-end;margin:8px 0'>
                <div style='background:#7c4dff;color:white;padding:12px 18px;
                border-radius:20px 20px 4px 20px;max-width:70%;font-size:15px;
                line-height:1.5;font-weight:500'>
                {msg["content"]}</div></div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='display:flex;justify-content:flex-start;margin:8px 0'>
                <div style='background:#fff8f9;color:#1a1a1a;padding:12px 18px;
                border-radius:20px 20px 20px 4px;max-width:74%;font-size:15px;
                line-height:1.7;border:1.5px solid #f5c6ce;
                box-shadow:0 2px 6px rgba(181,53,74,0.06)'>
                {msg["content"]}</div></div>
                """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Input
    with st.form("therapy_form", clear_on_submit=True):
        col1, col2 = st.columns([7, 1])
        with col1:
            user_input = st.text_input(
                "msg",
                placeholder="Share what you're feeling...",
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Send")

    if submitted and user_input and user_input.strip():
        st.session_state.therapy_history.append({
            "role": "user", "content": user_input
        })

        with st.spinner("Listening..."):
            try:
                messages = [{"role": "system", "content": THERAPY_SYSTEM}]
                for m in st.session_state.therapy_history:
                    role = "user" if m["role"] == "user" else "assistant"
                    messages.append({"role": role, "content": m["content"]})

                res = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.7
                )
                answer = res.choices[0].message.content
            except Exception as e:
                answer = f"Error: {e}"

        st.session_state.therapy_history.append({
            "role": "bot", "content": answer
        })
        st.rerun()

    # Breathing exercise — no expander to avoid overlap
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:white;border:1px solid #ede8e3;border-radius:12px;
    padding:20px;margin-top:8px'>
        <div style='font-size:14px;font-weight:700;color:#b5354a;
        margin-bottom:12px'>🫁 Calming Breathing Exercise</div>
        <div style='font-size:13px;color:#555;line-height:2'>
        <b>4-7-8 Technique:</b><br>
        1. Breathe in through nose for <b>4 seconds</b><br>
        2. Hold your breath for <b>7 seconds</b><br>
        3. Exhale slowly through mouth for <b>8 seconds</b><br>
        4. Repeat 3-4 times<br><br>
        <i>This technique reduces anxiety and stress immediately.</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.therapy_history:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat"):
            st.session_state.therapy_history = []
            st.rerun()