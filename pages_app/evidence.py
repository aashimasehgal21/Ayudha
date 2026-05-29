# pages_app/evidence.py

import streamlit as st
import openai
import os
import base64
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EVIDENCE_PROMPT = """
You are a legal evidence analyst helping a woman in India document a harassment incident.
Analyze this image carefully and provide:

1. WHAT IS VISIBLE: Describe exactly what you see (people, actions, location, any text/timestamps)
2. HARASSMENT INDICATOR: Is there evidence of harassment, threat, or assault? (Yes / No / Possibly)
3. EVIDENCE STRENGTH: Rate as Strong / Moderate / Weak / None
4. RELEVANT LAW: Which IPC section or law applies if harassment is visible
5. RECOMMENDED ACTION: What she should do next

Be factual, sensitive, and concise.
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
        font-weight:700;color:#1a1a1a;padding-top:4px'>🖼️ Evidence Analyzer</div>
        """, unsafe_allow_html=True)

    st.caption("Upload a photo or screenshot — AI will analyze it and provide legal guidance")
    st.divider()

    st.markdown("""
    <div style='background:#fdf0f2;border:1px solid #f5c6ce;border-radius:10px;
    padding:12px 18px;font-size:13px;color:#b5354a;margin-bottom:16px'>
    🔒 <b>Privacy:</b> Your image is only used for analysis — never stored or saved.
    Only image files are supported (JPG, PNG, WEBP).
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload image (CCTV screenshot, threatening message, injury photo)",
        type=["jpg", "jpeg", "png", "webp"],
    )

    if uploaded:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image(uploaded, caption="Uploaded image", use_container_width=True)
            st.markdown(f"""
            <div style='background:white;border:1px solid #ede8e3;
            border-radius:10px;padding:12px;margin-top:8px;
            font-size:13px;color:#555'>
            📁 <b>File:</b> {uploaded.name}<br>
            📊 <b>Size:</b> {round(uploaded.size/1024, 1)} KB
            </div>
            """, unsafe_allow_html=True)

        with col2:
            analyze_btn = st.button("🔍 Analyze Evidence", use_container_width=True)

            if analyze_btn:
                if uploaded.type not in ["image/jpeg", "image/png",
                                          "image/webp", "image/jpg"]:
                    st.error("Please upload an image file only (JPG, PNG, WEBP).")
                else:
                    with st.spinner("Analyzing image with AI..."):
                        try:
                            image_bytes = uploaded.read()
                            b64 = base64.b64encode(image_bytes).decode()
                            mime = uploaded.type

                            response = client.chat.completions.create(
                                model="gpt-4o",
                                messages=[{
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:{mime};base64,{b64}"
                                            }
                                        },
                                        {
                                            "type": "text",
                                            "text": EVIDENCE_PROMPT
                                        }
                                    ]
                                }],
                                max_tokens=1000
                            )

                            result = response.choices[0].message.content
                            st.session_state["evidence_result"] = result

                        except Exception as e:
                            st.error(f"Analysis failed: {e}")

            # Show result if available
            if "evidence_result" in st.session_state:
                result = st.session_state["evidence_result"]
                st.markdown("### 📋 Analysis Result")
                st.markdown(f"""
                <div style='background:#fff8f9;border:1.5px solid #f5c6ce;
                border-radius:12px;padding:20px;font-size:14px;
                line-height:1.8;color:#1a1a1a'>
                {result.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.download_button(
                    label="📥 Download Evidence Report",
                    data=result,
                    file_name="evidence_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

    else:
        # Clear old result when no file
        if "evidence_result" in st.session_state:
            del st.session_state["evidence_result"]

        st.markdown("""
        <div style='text-align:center;padding:40px 20px'>
            <div style='font-size:48px;margin-bottom:14px'>🖼️</div>
            <div style='font-size:15px;font-weight:600;color:#555'>
            Upload an image to analyze</div>
            <div style='font-size:13px;margin-top:8px;color:#aaa'>
            CCTV screenshots, threatening messages, injury photos</div>
        </div>
        """, unsafe_allow_html=True)