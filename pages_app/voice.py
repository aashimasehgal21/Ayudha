# pages_app/voice.py

from streamlit_mic_recorder import mic_recorder
import streamlit as st
import os
import tempfile
import requests
import re
from dotenv import load_dotenv
from openai import OpenAI

# ---------------- CONFIG ----------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

BACKEND = "http://127.0.0.1:8000"


# ---------------- CSS ----------------
def apply_css():

    st.markdown("""
    <style>

    /* GLOBAL TEXT */
    body, .stApp {
        color: #000 !important;
    }

    .stMarkdown, label, span, div, p {
        color: #000 !important;
    }

    h1, h2, h3 {
        color: #000 !important;
    }

    ::selection {
        background: transparent !important;
        color: #000 !important;
    }

    /* MIC BUTTON */
    button {
        color: white !important;
    }

    button p {
        color: white !important;
    }

    /* FILE UPLOADER FULL FIX */
    [data-testid="stFileUploader"] {
        color: white !important;
    }

    [data-testid="stFileUploader"] * {
        color: white !important;
    }

    [data-testid="stFileUploader"] small {
        color: #d1d5db !important;
    }

    /* DARK BOX TEXT */
    section[data-testid="stFileUploaderDropzone"] div,
    section[data-testid="stFileUploaderDropzone"] span,
    section[data-testid="stFileUploaderDropzone"] p,
    section[data-testid="stFileUploaderDropzone"] small {
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ---------------- CLEAN ANSWER ----------------
def clean_answer(text):

    return re.sub(
        r'\*?\*?SOURCE[S]?\*?\*?:.*',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    ).strip()


# ---------------- MAIN ----------------
def show():

    apply_css()

    st.title("🎙️ Voice Chat")

    st.caption(
        "Speak your legal query and get AI-powered guidance instantly"
    )

    st.divider()

    # ---------------- SESSION ----------------
    if "session_id" not in st.session_state:
        st.session_state.session_id = ""

    if "audio_file_path" not in st.session_state:
        st.session_state.audio_file_path = None

    # ---------------- INFO BOX ----------------
    st.markdown("""
    <div style='background:#ffffff;
    border:1.5px solid #f5c6ce;
    border-radius:12px;
    padding:15px;
    margin-bottom:20px;
    color:#000'>

    <b>How It Works:</b><br><br>

    🎤 Record your voice OR upload audio<br>
    🧠 AI converts speech to text<br>
    ⚖️ AYUDHA retrieves legal guidance<br>
    🔊 AI speaks the response back to you

    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # ---------------- MIC RECORDER ----------------
    # =========================================================

    st.markdown("### 🎤 Record Your Voice")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        use_container_width=True,
        key="mic"
    )

    if audio:

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".wav"
            ) as tmp:

                tmp.write(audio["bytes"])

                st.session_state.audio_file_path = tmp.name

            st.success("✅ Voice recorded successfully!")

            st.audio(
                audio["bytes"],
                format="audio/wav"
            )

        except Exception as e:

            st.error(f"Recording Error: {e}")

    st.divider()

    # =========================================================
    # ---------------- FILE UPLOAD ----------------
    # =========================================================

    st.markdown("### 📂 Or Upload Audio File")

    uploaded_file = st.file_uploader(
        "Upload voice file",
        type=["mp3", "wav", "m4a", "ogg", "webm"]
    )

    if uploaded_file:

        st.audio(uploaded_file)

        try:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{uploaded_file.name.split('.')[-1]}"
            ) as tmp:

                tmp.write(uploaded_file.read())

                st.session_state.audio_file_path = tmp.name

        except Exception as e:

            st.error(f"Upload Error: {e}")

    st.divider()

    # =========================================================
    # ---------------- PROCESS BUTTON ----------------
    # =========================================================

    if st.session_state.audio_file_path:

        if st.button(
            "🚀 Get Legal Answer",
            use_container_width=True
        ):

            with st.spinner("Processing your voice..."):

                try:

                    st.write("🎧 Transcribing audio...")

                    # =================================================
                    # SPEECH → TEXT
                    # =================================================

                    with open(st.session_state.audio_file_path, "rb") as f:

                        transcript = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=f
                        )

                    query = transcript.text

                    st.success("✅ Speech converted to text")

                    st.markdown(f"""
                    <div style='background:#fdf0f2;
                    border:1px solid #f5c6ce;
                    border-radius:10px;
                    padding:12px;
                    margin-bottom:12px;
                    color:#000'>

                    <b>🗣️ You said:</b><br><br>

                    {query}

                    </div>
                    """, unsafe_allow_html=True)

                    st.write("⚖️ Fetching legal guidance...")

                    # =================================================
                    # BACKEND API
                    # =================================================

                    response = requests.post(
                        f"{BACKEND}/chat",
                        json={
                            "query": query,
                            "session_id": st.session_state.session_id
                        },
                        timeout=60
                    )

                    data = response.json()

                    st.write("✅ Backend response received")

                    answer = clean_answer(
                        data.get(
                            "answer",
                            "Something went wrong"
                        )
                    )

                    st.session_state.session_id = data.get(
                        "session_id",
                        ""
                    )

                    # =================================================
                    # SHOW ANSWER
                    # =================================================

                    st.markdown(f"""
                    <div style='background:#ffffff;
                    color:#000;
                    padding:18px;
                    border-radius:12px;
                    border:1.5px solid #f5c6ce;
                    font-size:15px;
                    line-height:1.8'>

                    {answer}

                    </div>
                    """, unsafe_allow_html=True)

                    st.write("🔊 Generating AI voice response...")

                    # =================================================
                    # TEXT → SPEECH
                    # =================================================

                    tts = client.audio.speech.create(
                        model="tts-1",
                        voice="nova",
                        input=answer[:1000]
                    )

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".mp3"
                    ) as out:

                        out.write(tts.content)

                        out_path = out.name

                    st.markdown("### 🔊 Listen to AI Response")

                    with open(out_path, "rb") as f:

                        st.audio(
                            f.read(),
                            format="audio/mp3"
                        )

                    os.unlink(out_path)

                    # =================================================
                    # CLEANUP
                    # =================================================

                    if os.path.exists(st.session_state.audio_file_path):
                        os.unlink(st.session_state.audio_file_path)

                    st.session_state.audio_file_path = None

                except Exception as e:

                    st.error(f"Error: {e}")