# pages_app/timeline.py

import streamlit as st
import json
import os
from datetime import datetime, date
import openai
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
TIMELINE_FILE = "incident_timeline.json"


def load_incidents():
    if os.path.exists(TIMELINE_FILE):
        with open(TIMELINE_FILE, "r") as f:
            return json.load(f)
    return []


def save_incidents(incidents):
    with open(TIMELINE_FILE, "w") as f:
        json.dump(incidents, f, indent=2)


def generate_report(incidents):
    text = ""
    for i, inc in enumerate(incidents, 1):
        text += f"""
Incident {i}: Date={inc['date']}, Time={inc['time']},
Location={inc['location']}, Type={inc['incident_type']},
Description={inc['description']},
Witnesses={inc.get('witnesses','None')}, Evidence={inc.get('evidence','None')}
"""
    prompt = f"""Create a formal legal timeline report for a woman in India based on these incidents.
Include: summary of harassment pattern, chronological list, relevant IPC sections, recommended actions.
Make it formal and suitable for police/court submission.
Incidents: {text}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


def show():
    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Home"
            st.rerun()
    with col_title:
        st.markdown("""
        <div style='font-family:Playfair Display,serif;font-size:24px;
        font-weight:700;color:#1a1a1a;padding-top:4px'>📅 Incident Timeline</div>
        """, unsafe_allow_html=True)

    st.caption("Record every incident — serves as evidence in court or police")
    st.divider()

    incidents = load_incidents()
    tab1, tab2 = st.tabs(["➕ Add New Incident", "📋 View Timeline"])

    with tab1:
        st.markdown(
            "<div style='font-size:16px;font-weight:700;color:#1a1a1a;"
            "margin-bottom:16px'>Incident Details</div>",
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            inc_date = st.date_input("Date", value=date.today(), key="inc_date")
            inc_time = st.time_input("Time", value=datetime.now().time(), key="inc_time")
            location = st.text_input("Location", placeholder="Home, office, street...", key="inc_loc")
        with col2:
            incident_type = st.selectbox(
                "Type of incident",
                ["Physical harassment", "Verbal abuse", "Sexual harassment",
                 "Stalking", "Domestic violence", "Cyber harassment",
                 "Threatening", "Other"],
                key="inc_type"
            )
            witnesses = st.text_input("Witnesses (optional)", placeholder="Names if any", key="inc_wit")
            evidence  = st.text_input("Evidence available", placeholder="Photo, message, video...", key="inc_evi")

        description = st.text_area(
            "What happened — describe in detail",
            placeholder="Write everything in your own words...",
            height=120, key="inc_desc"
        )

        if st.button("💾 Save Incident", use_container_width=True):
            if not location or not description:
                st.error("Location and description are required.")
            else:
                new_incident = {
                    "id": len(incidents) + 1,
                    "date": str(inc_date),
                    "time": inc_time.strftime("%H:%M"),
                    "location": location,
                    "incident_type": incident_type,
                    "description": description,
                    "witnesses": witnesses or "None",
                    "evidence":  evidence or "None",
                    "saved_at": datetime.now().isoformat()
                }
                incidents.append(new_incident)
                save_incidents(incidents)
                st.success(f"✅ Incident #{new_incident['id']} saved!")
                st.rerun()

    with tab2:
        if not incidents:
            st.info("No incidents recorded yet. Use the Add tab above.")
        else:
            st.markdown(
                f"<div style='font-size:15px;font-weight:700;color:#1a1a1a;"
                f"margin-bottom:16px'>Total incidents: {len(incidents)}</div>",
                unsafe_allow_html=True
            )

            for inc in reversed(incidents):
                st.markdown(f"""
                <div style='background:#ffffff;border:1.5px solid #f5c6ce;
                border-radius:12px;padding:16px 20px;margin-bottom:12px'>
                    <div style='font-size:14px;font-weight:700;color:#b5354a;
                    margin-bottom:10px;padding-bottom:8px;
                    border-bottom:1px solid #fce8ec'>
                    Incident #{inc['id']} — {inc['date']} — {inc['incident_type']}
                    </div>
                    <div style='display:grid;grid-template-columns:1fr 1fr;
                    gap:6px;font-size:13px;color:#1a1a1a;margin-bottom:8px'>
                        <div>📅 <b>Date:</b> {inc['date']}</div>
                        <div>⚠️ <b>Type:</b> {inc['incident_type']}</div>
                        <div>🕐 <b>Time:</b> {inc['time']}</div>
                        <div>👁️ <b>Witnesses:</b> {inc.get('witnesses','None')}</div>
                        <div>📍 <b>Location:</b> {inc['location']}</div>
                        <div>📎 <b>Evidence:</b> {inc.get('evidence','None')}</div>
                    </div>
                    <div style='font-size:13px;color:#1a1a1a'>
                    📝 <b>Description:</b> {inc['description']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"🗑️ Delete #{inc['id']}", key=f"del_{inc['id']}"):
                    incidents = [x for x in incidents if x['id'] != inc['id']]
                    save_incidents(incidents)
                    st.rerun()

            st.divider()

            if st.button("📄 Generate Legal Report", use_container_width=True):
                with st.spinner("⏳ Ayudha is answering..."):
                    try:
                        report = generate_report(incidents)
                        st.session_state["timeline_report"] = report
                    except Exception as e:
                        st.error(f"Error: {e}")

            if "timeline_report" in st.session_state:
                report = st.session_state["timeline_report"]
                st.markdown(
                    "<div style='font-size:16px;font-weight:700;color:#1a1a1a;"
                    "margin:16px 0 8px'>📋 Legal Timeline Report</div>",
                    unsafe_allow_html=True
                )
                st.markdown(f"""
                <div style='background:#ffffff;border:1.5px solid #f5c6ce;
                border-radius:12px;padding:20px;font-size:14px;
                line-height:1.8;color:#1a1a1a;white-space:pre-wrap'>
                {report}
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>**Download report:**", unsafe_allow_html=False)
                dl1, dl2 = st.columns(2)
                with dl1:
                    st.download_button(
                        label="📥 Download TXT",
                        data=report,
                        file_name=f"timeline_{date.today()}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with dl2:
                    try:
                        from reportlab.lib.pagesizes import A4
                        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                        from reportlab.lib.units import inch
                        from reportlab.lib import colors
                        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
                        import tempfile, os as _os

                        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                        tmp_path = tmp.name; tmp.close()
                        doc2 = SimpleDocTemplate(tmp_path, pagesize=A4,
                            rightMargin=0.8*inch, leftMargin=0.8*inch,
                            topMargin=0.8*inch, bottomMargin=0.8*inch)
                        s = getSampleStyleSheet()
                        s.add(ParagraphStyle("T", fontSize=10, fontName="Helvetica",
                            leading=16, spaceAfter=6))
                        elems = [
                            Paragraph("AYUDHA — Incident Timeline Report",
                                ParagraphStyle("H", fontSize=18, fontName="Helvetica-Bold",
                                textColor=colors.HexColor("#b5354a"), alignment=1, spaceAfter=12)),
                            HRFlowable(width="100%", thickness=1.5,
                                color=colors.HexColor("#b5354a"), spaceAfter=12)
                        ]
                        for line in report.split("\n"):
                            line = line.strip()
                            if not line: elems.append(Spacer(1, 5))
                            else: elems.append(Paragraph(line, s["T"]))
                        doc2.build(elems)
                        with open(tmp_path, "rb") as pf:
                            pdf_bytes = pf.read()
                        _os.unlink(tmp_path)
                        st.download_button(
                            label="📄 Download PDF",
                            data=pdf_bytes,
                            file_name=f"timeline_{date.today()}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except Exception as pe:
                        st.warning(f"PDF error: {pe}")