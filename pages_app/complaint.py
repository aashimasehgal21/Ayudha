# pages_app/complaint.py

import streamlit as st
import openai
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_complaint(details: dict, doc_type: str) -> str:
    prompt = f"""
You are a legal document writer helping a woman in India.
Generate a formal {doc_type} in English based on these details:

Complainant Name: {details['name']}
Date of Incident: {details['incident_date']}
Location: {details['location']}
Accused Name/Description: {details['accused']}
What Happened: {details['description']}
Witnesses (if any): {details['witnesses']}

Requirements:
- Use proper legal language
- Mention relevant IPC sections automatically
- Format properly with To, From, Subject, Body, Date
- End with signature block
- Keep it factual and professional
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def create_pdf(details, draft, doc_type):
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
        import tempfile
        import os as _os
        from datetime import datetime

        BRAND_RED = colors.HexColor("#b5354a")
        BRAND_LIGHT = colors.HexColor("#fdf0f2")
        DARK = colors.HexColor("#1a1a1a")
        GRAY = colors.HexColor("#666666")
        LIGHT_GRAY = colors.HexColor("#f5f5f5")

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_path = tmp.name
        tmp.close()

        doc = SimpleDocTemplate(tmp_path, pagesize=A4,
            rightMargin=0.8*inch, leftMargin=0.8*inch,
            topMargin=0.8*inch, bottomMargin=0.8*inch)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle("ATitle", fontSize=22, fontName="Helvetica-Bold",
            textColor=BRAND_RED, alignment=1, spaceAfter=4))
        styles.add(ParagraphStyle("ASub", fontSize=11, fontName="Helvetica",
            textColor=GRAY, alignment=1, spaceAfter=2))
        styles.add(ParagraphStyle("DTitle", fontSize=16, fontName="Helvetica-Bold",
            textColor=DARK, alignment=1, spaceBefore=12, spaceAfter=8))
        styles.add(ParagraphStyle("SHead", fontSize=12, fontName="Helvetica-Bold",
            textColor=BRAND_RED, spaceBefore=12, spaceAfter=4))
        styles.add(ParagraphStyle("BText", fontSize=10, fontName="Helvetica",
            textColor=DARK, leading=16, alignment=4, spaceAfter=6))
        styles.add(ParagraphStyle("SGray", fontSize=9, fontName="Helvetica",
            textColor=GRAY, spaceAfter=4))
        styles.add(ParagraphStyle("Foot", fontSize=8, fontName="Helvetica",
            textColor=GRAY, alignment=1))

        elems = []
        elems.append(Paragraph("AYUDHA", styles["ATitle"]))
        elems.append(Paragraph("Women's Legal Assistant — Confidential Document", styles["ASub"]))
        elems.append(HRFlowable(width="100%", thickness=1.5, color=BRAND_RED, spaceAfter=12))
        elems.append(Paragraph(doc_type.upper(), styles["DTitle"]))
        elems.append(Paragraph(
            f"Date Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            styles["SGray"]))
        elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=10))
        elems.append(Paragraph("Complainant Details", styles["SHead"]))

        rows = [
            ("Complainant Name", details.get("name", "—")),
            ("Date of Incident", details.get("incident_date", "—")),
            ("Location", details.get("location", "—")),
            ("Accused", details.get("accused", "—")),
            ("Witnesses", details.get("witnesses", "None")),
        ]
        tbl = Table(
            [[Paragraph(f"<b>{r[0]}</b>", styles["BText"]),
              Paragraph(str(r[1]), styles["BText"])] for r in rows],
            colWidths=[2*inch, 4.5*inch]
        )
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (0,-1), BRAND_LIGHT),
            ("ROWBACKGROUNDS", (1,0), (1,-1), [colors.white, LIGHT_GRAY]),
            ("BOX", (0,0), (-1,-1), 0.5, colors.lightgrey),
            ("INNERGRID", (0,0), (-1,-1), 0.3, colors.lightgrey),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING", (0,0), (-1,-1), 8),
        ]))
        elems.append(tbl)
        elems.append(Spacer(1, 12))
        elems.append(Paragraph("Draft Content", styles["SHead"]))
        elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=8))

        for line in draft.split("\n"):
            line = line.strip()
            if not line:
                elems.append(Spacer(1, 6))
            elif line.startswith(("To,", "From,", "Subject:", "Date:", "Respected")):
                elems.append(Paragraph(f"<b>{line}</b>", styles["BText"]))
            else:
                elems.append(Paragraph(line, styles["BText"]))

        elems.append(Spacer(1, 20))
        elems.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey, spaceAfter=6))
        elems.append(Paragraph(
            "Generated by Ayudha — Women's Legal Assistant. Review with a legal professional.",
            styles["Foot"]))

        doc.build(elems)
        with open(tmp_path, "rb") as f:
            pdf_bytes = f.read()
        _os.unlink(tmp_path)
        return pdf_bytes
    except Exception as e:
        st.warning(f"PDF error: {e}")
        return None


def show():
    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Home"
            st.rerun()
    with col_title:
        st.markdown("""
        <div style='font-family:Playfair Display,serif;font-size:24px;
        font-weight:700;color:#1a1a1a;padding-top:4px'>📋 Complaint Draft Generator</div>
        """, unsafe_allow_html=True)

    st.caption("Fill in details — AI generates a complete legal document instantly")
    st.divider()

    doc_type = st.selectbox("Document type", [
        "FIR (First Information Report)",
        "Police Complaint Letter",
        "Legal Notice",
        "Workplace Harassment Complaint (POSH)",
        "Court Complaint"
    ])

    col1, col2 = st.columns(2)
    with col1:
        name          = st.text_input("Your full name *", placeholder="Full name")
        incident_date = st.date_input("Date of incident *", value=date.today())
        location      = st.text_input("Location *", placeholder="Where did it happen")
    with col2:
        accused   = st.text_input("Accused name/description", placeholder="Name or description")
        witnesses = st.text_input("Witnesses (optional)", placeholder="Any witnesses")

    description = st.text_area(
        "What happened — describe in detail *",
        placeholder="Write everything in your own words...",
        height=150
    )

    st.divider()

    if st.button("📝 Generate Draft", use_container_width=True):
        if not name or not location or not description:
            st.error("Name, location and description are required.")
        else:
            with st.spinner("⏳ Ayudha is answering..."):
                try:
                    details = {
                        "name": name,
                        "incident_date": str(incident_date),
                        "location": location,
                        "accused": accused or "Unknown",
                        "witnesses": witnesses or "None",
                        "description": description,
                        "doc_type": doc_type
                    }
                    draft = generate_complaint(details, doc_type)
                    st.session_state["complaint_draft"] = draft
                    st.session_state["complaint_details"] = details
                except Exception as e:
                    st.error(f"Error: {e}")

    # Show draft if available
    if "complaint_draft" in st.session_state:
        draft = st.session_state["complaint_draft"]
        details = st.session_state.get("complaint_details", {})

        st.success("✅ Draft ready!")
        st.markdown("### 📄 Generated Draft")
        st.markdown(f"""
        <div style='background:#ffffff;border:1.5px solid #f5c6ce;
        border-radius:12px;padding:24px;font-size:14px;
        line-height:1.8;color:#1a1a1a;white-space:pre-wrap'>
        {draft}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**Download your draft:**")

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download as TXT",
                data=draft,
                file_name=f"complaint_{date.today()}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col2:
            pdf = create_pdf(details, draft, details.get("doc_type", "Complaint"))
            if pdf:
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf,
                    file_name=f"complaint_{date.today()}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )