# app.py

import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Ayudha - Women's Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@400;500;600&display=swap');

/* ── FORCE LIGHT MODE ── */
html, body { color-scheme: light !important; }

[data-testid="stAppViewContainer"] { background: #faf7f4 !important; }
[data-testid="stMain"] { background: #faf7f4 !important; }
section[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #ede8e3 !important;
}

/* Force ALL text dark */
p, span, label, div, h1, h2, h3, h4, h5, li, a {
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] span {
    color: #1a1a1a !important;
}

/* Caption */
[data-testid="stCaptionContainer"] p { color: #888 !important; }

/* Input boxes */
input, textarea {
    background: white !important;
    color: #1a1a1a !important;
    border: 1px solid #ede8e3 !important;
    border-radius: 8px !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background: white !important;
    color: #1a1a1a !important;
    border: 1px solid #ede8e3 !important;
    border-radius: 8px !important;
}
div[data-baseweb="select"] span {
    color: #1a1a1a !important;
}

/* Dropdown popup */
div[data-baseweb="popover"] {
    background: white !important;
}
div[data-baseweb="popover"] * {
    background: white !important;
    color: #1a1a1a !important;
}
div[data-baseweb="menu"] {
    background: white !important;
}
div[data-baseweb="menu"] li {
    color: #1a1a1a !important;
    background: white !important;
}
div[data-baseweb="menu"] li:hover {
    background: #fdf0f2 !important;
    color: #b5354a !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] {
    background: white !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] li {
    color: #1a1a1a !important;
    background: white !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] li:hover {
    background: #fdf0f2 !important;
    color: #b5354a !important;
}

/* Multiselect */
div[data-baseweb="tag"] {
    background: #fdf0f2 !important;
}
div[data-baseweb="tag"] span { color: #b5354a !important; }

/* Tabs */
div[data-baseweb="tab-list"] { background: transparent !important; }
div[data-baseweb="tab"] { color: #555 !important; }
div[data-baseweb="tab"][aria-selected="true"] {
    color: #b5354a !important;
    border-bottom: 2px solid #b5354a !important;
}

/* Expander */
div[data-testid="stExpander"] {
    background: white !important;
    border: 1px solid #ede8e3 !important;
    border-radius: 12px !important;
}
div[data-testid="stExpander"] summary {
    color: #1a1a1a !important;
    background: #fdf0f2 !important;
}
div[data-testid="stExpander"] > div {
    background: white !important;
    color: #1a1a1a !important;
}

/* Divider */
hr { border-color: #ede8e3 !important; }

/* ── ALL BUTTONS default pink ── */
.stButton > button {
    background: #fdf0f2 !important;
    color: #b5354a !important;
    border: 1px solid #f5c6ce !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    min-height: unset !important;
    padding: 8px 16px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #f9e0e4 !important;
    border-color: #b5354a !important;
}

/* Send button red */
div[data-testid="stFormSubmitButton"] > button {
    background: #b5354a !important;
    color: white !important;
    border: none !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #9a2a3d !important;
}

/* ── FEATURE CARDS ── */
.feat-card {
    background: white !important;
    border: 1.5px solid #ede8e3;
    border-radius: 18px;
    padding: 28px 16px 20px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    margin-bottom: 4px;
    min-height: 185px;
    transition: all 0.25s;
}
.feat-card:hover {
    border-color: #b5354a;
    box-shadow: 0 8px 28px rgba(181,53,74,0.12);
    transform: translateY(-3px);
}
.feat-icon { font-size: 36px; margin-bottom: 12px; display: block; }
.feat-name {
    font-size: 15px !important;
    font-weight: 700 !important;
    color: #1a1a1a !important;
    margin-bottom: 7px;
}
.feat-desc {
    font-size: 12px !important;
    color: #777 !important;
    line-height: 1.6;
}
.feat-open-btn button {
    background: #fdf0f2 !important;
    color: #b5354a !important;
    border: 1px solid #f5c6ce !important;
    border-radius: 8px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 6px 12px !important;
    min-height: unset !important;
    width: 100% !important;
}
.feat-open-btn button:hover { background: #f9e0e4 !important; }

/* ── NEWS CARD ── */
.news-slide {
    background: white;
    border-radius: 20px;
    overflow: hidden;
    border: 1px solid #ede8e3;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    margin-bottom: 12px;
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    min-height: 300px;
}
.news-img {
    width: 100%; height: 100%;
    min-height: 300px;
    object-fit: cover; display: block;
}
.news-body {
    padding: 32px 28px;
    display: flex; flex-direction: column;
    justify-content: center;
    background: white;
}
.news-source-tag {
    display: inline-block;
    background: #fdf0f2; color: #b5354a !important;
    font-size: 11px; font-weight: 700;
    padding: 4px 12px; border-radius: 20px;
    text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 14px; width: fit-content;
}
.news-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 20px; font-weight: 700;
    color: #1a1a1a !important; line-height: 1.5;
    margin-bottom: 12px;
}
.news-meta { font-size: 12px; color: #aaa !important; }

/* ── NAV DOTS ── */
.nav-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%; margin: 0 4px;
    background: #ddd;
}
.nav-dot.active {
    background: #b5354a;
    width: 22px; border-radius: 4px;
}

/* ── SECTION TITLE ── */
.sec-title {
    font-family: 'Playfair Display', serif !important;
    font-size: 22px; font-weight: 700;
    color: #1a1a1a !important; margin-bottom: 18px;
}

/* ── SOS BAR ── */
.sos-bar {
    background: linear-gradient(135deg, #b5354a, #d4637a);
    text-align: center;
    padding: 14px 20px; border-radius: 14px;
    font-size: 13px; font-weight: 600;
    margin-top: 32px;
    box-shadow: 0 4px 16px rgba(181,53,74,0.2);
}
.sos-bar, .sos-bar * { color: white !important; }

/* ── SIDEBAR NAV ACTIVE ── */
.nav-active {
    background: #fdf0f2;
    border: 1px solid #f5c6ce;
    border-radius: 10px; padding: 10px 16px;
    font-weight: 700; font-size: 14px;
    margin-bottom: 6px;
}
.nav-active, .nav-active * { color: #b5354a !important; }

/* ── CHAT BUBBLES ── */
.user-bubble {
    background: #b5354a !important;
    padding: 13px 18px;
    border-radius: 20px 20px 4px 20px;
    max-width: 70%; font-size: 15px;
    line-height: 1.5; font-weight: 500;
    box-shadow: 0 2px 8px rgba(181,53,74,0.25);
    margin-left: auto;
}
.user-bubble, .user-bubble * { color: white !important; }

.bot-bubble {
    background: #fff8f9 !important;
    padding: 14px 20px;
    border-radius: 20px 20px 20px 4px;
    max-width: 74%; font-size: 15px;
    line-height: 1.7;
    border: 1.5px solid #f5c6ce !important;
    box-shadow: 0 2px 8px rgba(181,53,74,0.06);
}
.bot-bubble, .bot-bubble * { color: #1a1a1a !important; }
/* Download buttons — always visible */
div[data-testid="stDownloadButton"] > button {
    background: #fdf0f2 !important;
    color: #b5354a !important;
    border: 1px solid #f5c6ce !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    width: 100% !important;
    padding: 10px 16px !important;
    min-height: unset !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: #f9e0e4 !important;
    border-color: #b5354a !important;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "news_index" not in st.session_state:
    st.session_state.news_index = 0

# ── News data ──
GOOD_IMAGES = [
    "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=700&q=80",
    "https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=700&q=80",
    "https://images.unsplash.com/photo-1505664194779-8beaceb93744?w=700&q=80",
    "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=700&q=80",
    "https://images.unsplash.com/photo-1521791136064-7986c2920216?w=700&q=80",
    "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=700&q=80",
    "https://images.unsplash.com/photo-1593115057322-e94b77572f20?w=700&q=80",
]

FALLBACK_NEWS = [
    {"source": "Supreme Court of India",
     "title": "SC directs all states to set up fast-track courts for sexual harassment cases within 3 months",
     "image": GOOD_IMAGES[0], "date": "17 Mar 2026"},
    {"source": "Ministry of Women & Child",
     "title": "Mission Shakti launched — integrated scheme for women safety and empowerment across India",
     "image": GOOD_IMAGES[1], "date": "15 Mar 2026"},
    {"source": "Delhi High Court",
     "title": "Employers must resolve POSH complaints within 90 days or face contempt proceedings",
     "image": GOOD_IMAGES[2], "date": "14 Mar 2026"},
    {"source": "National Commission for Women",
     "title": "NCW records 30% rise in cyberstalking complaints — urges stronger IT Act enforcement",
     "image": GOOD_IMAGES[3], "date": "12 Mar 2026"},
    {"source": "Bombay High Court",
     "title": "FIR must be registered immediately in domestic violence cases — no mediation first",
     "image": GOOD_IMAGES[4], "date": "10 Mar 2026"},
    {"source": "NALSA",
     "title": "Free legal aid available to all women at every District Legal Services Authority in India",
     "image": GOOD_IMAGES[5], "date": "8 Mar 2026"},
    {"source": "Ministry of Home Affairs",
     "title": "Police must record women complaints within 24 hours or face departmental action",
     "image": GOOD_IMAGES[6], "date": "5 Mar 2026"},
]

@st.cache_data(ttl=1800)
def fetch_news():
    try:
        API_KEY = os.getenv("NEWS_API_KEY")
        if not API_KEY:
            return FALLBACK_NEWS
        r = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": "women harassment law India rights IPC",
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 7,
                "apiKey": API_KEY,
                "domains": "thehindu.com,ndtv.com,timesofindia.indiatimes.com,hindustantimes.com,indianexpress.com,livelaw.in,barandbench.com"
            }, timeout=5
        )
        articles = r.json().get("articles", [])
        result = []
        for i, a in enumerate(articles):
            title = a.get("title", "")
            if not title or "[Removed]" in title:
                continue
            img = a.get("urlToImage")
            if not img or "http" not in img:
                img = GOOD_IMAGES[i % len(GOOD_IMAGES)]
            result.append({
                "source": a.get("source", {}).get("name", "India News"),
                "title": title,
                "image": img,
                "date": a.get("publishedAt", "")[:10]
            })
        return result if len(result) >= 3 else FALLBACK_NEWS
    except Exception:
        return FALLBACK_NEWS

NEWS = fetch_news()

# ── Sidebar ──
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:28px 16px 22px;
    border-bottom:1px solid #ede8e3;background:white'>
        <div style='font-size:42px'>⚖️</div>
        <div style='font-family:Playfair Display,serif;font-size:26px;
        font-weight:700;color:#b5354a'>AYUDHA</div>
        <div style='font-size:12px;color:#aaa;margin-top:4px'>
        Women's Legal Assistant</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding:12px 10px 8px;background:white'>",
                unsafe_allow_html=True)

    PAGES = [
        ("🏠", "Home"), ("💬", "Legal Chat"),
        ("🎙️", "Voice Chat"), ("🖼️", "Evidence Analyzer"),
        ("📋", "Complaint Draft"), ("📅", "Incident Timeline"),
        ("🧘", "Emotional Support"), ("🏛️", "NGO Finder"),
    ]

    for icon, name in PAGES:
        if st.session_state.page == name:
            st.markdown(
                f"<div class='nav-active'>{icon} &nbsp; {name}</div>",
                unsafe_allow_html=True
            )
        else:
            if st.button(f"{icon}  {name}", key=f"nav_{name}",
                         width="stretch"):
                st.session_state.page = name
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("""
    <div style='padding:4px 16px 20px;background:white'>
    <div style='font-size:11px;font-weight:700;color:#b5354a;
    margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px'>
    Emergency Helplines</div>
    <div style='font-size:13px;color:#444;line-height:2.4'>
    🆘 <b>112</b> — Emergency<br>
    👩 <b>1091</b> — Women Helpline<br>
    🏠 <b>181</b> — Domestic Violence<br>
    👶 <b>1098</b> — Child Helpline<br>
    ⚖️ <b>15100</b> — Legal Aid
    </div></div>
    """, unsafe_allow_html=True)

# ── HOME ──
if st.session_state.page == "Home":

    st.markdown('<div class="sec-title">Latest Legal Updates</div>',
                unsafe_allow_html=True)

    idx = st.session_state.news_index % len(NEWS)
    n = NEWS[idx]

    st.markdown(f"""
    <div class="news-slide">
        <img class="news-img" src="{n['image']}" alt="">
        <div class="news-body">
            <span class="news-source-tag">{n['source']}</span>
            <div class="news-title">{n['title']}</div>
            <div class="news-meta">📅 {n['date']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    dots = "".join([
        f'<span class="nav-dot {"active" if i == idx else ""}"></span>'
        for i in range(len(NEWS))
    ])
    st.markdown(
        f"<div style='text-align:center;margin:6px 0 4px'>{dots}</div>",
        unsafe_allow_html=True
    )

    c1, _, c3 = st.columns([2, 6, 2])
    with c1:
        if st.button("◀  Prev", width="stretch", key="news_prev"):
            st.session_state.news_index -= 1
            st.rerun()
    with c3:
        if st.button("Next  ▶", width="stretch", key="news_next"):
            st.session_state.news_index += 1
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">How Can Ayudha Help You?</div>',
                unsafe_allow_html=True)

    FEATURES = [
        ("💬", "Legal Chat",
         "Ask any legal question — IPC sections, rights & guidance", "Legal Chat"),
        ("🎙️", "Voice Chat",
         "Speak your question — Ayudha listens and speaks back", "Voice Chat"),
        ("🖼️", "Evidence Analyzer",
         "Upload photo or screenshot — AI identifies legal evidence", "Evidence Analyzer"),
        ("📋", "Complaint Draft",
         "Generate FIR, complaint letter or legal notice instantly", "Complaint Draft"),
        ("📅", "Incident Timeline",
         "Log incidents over time — build a legal record for court", "Incident Timeline"),
        ("🧘", "Emotional Support",
         "Talk freely — compassionate support, no judgment", "Emotional Support"),
        ("🏛️", "NGO Finder",
         "Find free legal aid, shelters & helplines near you", "NGO Finder"),
        ("🔒", "Anonymous & Safe",
         "No login needed — conversations stay private", None),
    ]

    row1 = st.columns(4)
    row2 = st.columns(4)

    for i, (icon, name, desc, nav) in enumerate(FEATURES):
        col = row1[i] if i < 4 else row2[i - 4]
        with col:
            st.markdown(f"""
            <div class="feat-card">
                <span class="feat-icon">{icon}</span>
                <div class="feat-name">{name}</div>
                <div class="feat-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if nav:
                st.markdown('<div class="feat-open-btn">', unsafe_allow_html=True)
                if st.button(f"Open →", key=f"fc_{i}",
                             width="stretch"):
                    st.session_state.page = nav
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

# ── Feature pages ──
elif st.session_state.page == "Legal Chat":
    from pages_app.chat import show; show()

elif st.session_state.page == "Voice Chat":
    from pages_app.voice import show; show()

elif st.session_state.page == "Evidence Analyzer":
    from pages_app.evidence import show; show()

elif st.session_state.page == "Complaint Draft":
    from pages_app.complaint import show; show()

elif st.session_state.page == "Incident Timeline":
    from pages_app.timeline import show; show()

elif st.session_state.page == "Emotional Support":
    from pages_app.therapy import show; show()

elif st.session_state.page == "NGO Finder":
    from pages_app.ngo import show; show()

# ── SOS bar ──
st.markdown("""
<div class="sos-bar">
    🆘 EMERGENCY: 112 &nbsp;|&nbsp;
    👩 WOMEN HELPLINE: 1091 &nbsp;|&nbsp;
    🏠 DOMESTIC VIOLENCE: 181 &nbsp;|&nbsp;
    ⚖️ LEGAL AID: 15100
</div>
""", unsafe_allow_html=True)