# pages_app/ngo.py

import streamlit as st

# All India NGO database
ALL_NGOS = {
    "Delhi": [
        {"name": "Sakshi NGO", "phone": "011-26853846", "service": "Legal aid, counseling", "address": "New Delhi"},
        {"name": "Jagori", "phone": "011-26692700", "service": "Women safety, legal help", "address": "New Delhi"},
        {"name": "CREA", "phone": "011-43087601", "service": "Rights, legal support", "address": "New Delhi"},
        {"name": "Delhi Commission for Women", "phone": "011-23379181", "service": "Legal aid, FIR help", "address": "New Delhi"},
    ],
    "Mumbai": [
        {"name": "iCall", "phone": "9152987821", "service": "Mental health, counseling", "address": "Mumbai"},
        {"name": "SNDT Women's University Legal Aid", "phone": "022-26600235", "service": "Free legal aid", "address": "Mumbai"},
        {"name": "Majlis Legal Centre", "phone": "022-23728080", "service": "Legal aid for women", "address": "Mumbai"},
        {"name": "Akshara Centre", "phone": "022-23098308", "service": "Violence against women", "address": "Mumbai"},
    ],
    "Bangalore": [
        {"name": "Vanitha Sahayavani", "phone": "080-22943225", "service": "Women helpline", "address": "Bangalore"},
        {"name": "Parihar", "phone": "080-22943225", "service": "Domestic violence help", "address": "Bangalore"},
        {"name": "Samvada", "phone": "080-25496101", "service": "Counseling, legal aid", "address": "Bangalore"},
    ],
    "Chennai": [
        {"name": "SNEHI", "phone": "044-24640050", "service": "Crisis support", "address": "Chennai"},
        {"name": "Tulir", "phone": "044-45034567", "service": "Child abuse prevention", "address": "Chennai"},
        {"name": "Tamil Nadu Women Helpline", "phone": "044-28592750", "service": "Legal aid, shelter", "address": "Chennai"},
    ],
    "Hyderabad": [
        {"name": "SHE Teams", "phone": "100", "service": "Women safety patrol", "address": "Hyderabad"},
        {"name": "Prajwala", "phone": "040-23548366", "service": "Rescue, rehabilitation", "address": "Hyderabad"},
        {"name": "Anveshi", "phone": "040-27638787", "service": "Legal research, aid", "address": "Hyderabad"},
    ],
    "Kolkata": [
        {"name": "Swayam", "phone": "033-24551176", "service": "Women's rights, legal aid", "address": "Kolkata"},
        {"name": "Sanhita", "phone": "033-24860114", "service": "Legal aid, counseling", "address": "Kolkata"},
        {"name": "WBCSW Helpline", "phone": "1800-345-8989", "service": "Women helpline", "address": "West Bengal"},
    ],
    "Pune": [
        {"name": "Stree Mukti Sanghatna", "phone": "020-24485376", "service": "Women's rights", "address": "Pune"},
        {"name": "MAVA", "phone": "020-25536395", "service": "Legal aid, shelter", "address": "Pune"},
    ],
    "Ahmedabad": [
        {"name": "Aman Samaaj", "phone": "079-26577759", "service": "Legal aid, counseling", "address": "Ahmedabad"},
        {"name": "SEWA", "phone": "079-25506477", "service": "Women empowerment", "address": "Ahmedabad"},
    ],
    "Jaipur": [
        {"name": "Vishakha", "phone": "0141-2741000", "service": "Legal aid, POSH", "address": "Jaipur"},
        {"name": "RPWDC Helpline", "phone": "1800-180-6785", "service": "Women helpline", "address": "Rajasthan"},
    ],
    "Lucknow": [
        {"name": "UP Mahila Helpline", "phone": "1090", "service": "Women safety, legal help", "address": "UP"},
        {"name": "Nari Shakti", "phone": "0522-2305399", "service": "Legal aid, counseling", "address": "Lucknow"},
    ],
}

NATIONAL_HELPLINES = [
    {"name": "National Commission for Women", "phone": "7827170170", "service": "Legal aid, complaints", "address": "National"},
    {"name": "Women Helpline (National)", "phone": "1091", "service": "24x7 emergency help", "address": "Pan India"},
    {"name": "One Stop Centre (Sakhi)", "phone": "181", "service": "Shelter, legal, medical", "address": "All states"},
    {"name": "iCall (Online)", "phone": "9152987821", "service": "Mental health support", "address": "Pan India"},
    {"name": "NALSA Legal Aid", "phone": "15100", "service": "Free legal aid", "address": "Pan India"},
]


def show():
    col_back, col_title = st.columns([1, 8])
    with col_back:
        if st.button("← Back"):
            st.session_state.page = "Home"
            st.rerun()
    with col_title:
        st.markdown("""
        <div style='font-family:Playfair Display,serif;font-size:24px;
        font-weight:700;color:#1a1a1a;padding-top:4px'>🏛️ NGO & Legal Aid Finder</div>
        """, unsafe_allow_html=True)

    st.caption("Find NGOs, legal aid centres and helplines near you")
    st.divider()

    # Emergency strip
    st.markdown("""
    <div style='background:#b5354a;color:white;padding:12px 20px;
    border-radius:10px;text-align:center;font-weight:600;
    font-size:13px;margin-bottom:20px'>
    🆘 112 &nbsp;|&nbsp; 👩 Women: 1091 &nbsp;|&nbsp;
    🏠 DV: 181 &nbsp;|&nbsp; 👶 Child: 1098 &nbsp;|&nbsp; ⚖️ Legal Aid: 15100
    </div>
    """, unsafe_allow_html=True)

    # Search by city name — free text
    col1, col2 = st.columns([3, 1])
    with col1:
        search_city = st.text_input(
            "Search your city",
            placeholder="Type city name (e.g. Delhi, Mumbai, Chennai...)",
            key="ngo_city_search"
        )
    with col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        search_btn = st.button("🔍 Search", use_container_width=True)

    # Also show dropdown
    selected_city = st.selectbox(
        "Or select from list",
        ["— Select city —"] + sorted(ALL_NGOS.keys()) + ["All National Helplines"],
        key="ngo_city_select"
    )

    st.divider()

    # Determine which city to show
    show_city = None
    ngos_to_show = []

    if search_btn and search_city.strip():
        # Search by text
        city_input = search_city.strip().title()
        if city_input in ALL_NGOS:
            show_city = city_input
            ngos_to_show = ALL_NGOS[city_input] + NATIONAL_HELPLINES
        else:
            # Partial match
            matches = [c for c in ALL_NGOS if city_input.lower() in c.lower()]
            if matches:
                show_city = matches[0]
                ngos_to_show = ALL_NGOS[matches[0]] + NATIONAL_HELPLINES
            else:
                st.warning(f"No results for '{city_input}'. Showing national helplines.")
                ngos_to_show = NATIONAL_HELPLINES
                show_city = "National"

    elif selected_city not in ["— Select city —", None]:
        if selected_city == "All National Helplines":
            ngos_to_show = NATIONAL_HELPLINES
            show_city = "National"
        else:
            show_city = selected_city
            ngos_to_show = ALL_NGOS.get(selected_city, []) + NATIONAL_HELPLINES

    if ngos_to_show:
        st.markdown(
            f"<div style='font-size:15px;font-weight:700;color:#1a1a1a;"
            f"margin-bottom:16px'>📍 {show_city} — {len(ngos_to_show)} resources found</div>",
            unsafe_allow_html=True
        )

        for ngo in ngos_to_show:
            st.markdown(f"""
            <div style='background:#ffffff;border:1px solid #ede8e3;
            border-radius:12px;padding:16px 20px;margin-bottom:10px;
            box-shadow:0 2px 8px rgba(0,0,0,0.04)'>
                <div style='display:flex;justify-content:space-between;
                align-items:center;flex-wrap:wrap;gap:8px'>
                    <div>
                        <div style='font-size:15px;font-weight:700;
                        color:#1a1a1a;margin-bottom:4px'>{ngo['name']}</div>
                        <div style='font-size:12px;color:#777'>{ngo['service']}</div>
                        <div style='font-size:12px;color:#aaa;margin-top:2px'>
                        📍 {ngo['address']}</div>
                    </div>
                    <div style='background:#fdf0f2;border:1px solid #f5c6ce;
                    border-radius:8px;padding:8px 16px;text-align:center;min-width:90px'>
                        <div style='font-size:11px;color:#b5354a;
                        font-weight:700;margin-bottom:2px'>📞 CALL</div>
                        <div style='font-size:16px;font-weight:700;
                        color:#b5354a'>{ngo['phone']}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align:center;padding:30px;color:#888'>
            <div style='font-size:40px;margin-bottom:12px'>🔍</div>
            <div style='font-size:15px;color:#555'>Search your city above to find local NGOs</div>
        </div>
        """, unsafe_allow_html=True)

    # Free Legal Aid section
    st.divider()
    st.markdown(
        "<div style='font-size:16px;font-weight:700;color:#1a1a1a;"
        "margin-bottom:12px'>🆓 Free Legal Aid</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div style='background:#ffffff;border:1.5px solid #f5c6ce;
    border-radius:12px;padding:20px;font-size:14px;color:#1a1a1a;line-height:2.2'>
    • <b>District Legal Services Authority (DLSA)</b> — Free legal aid in every district<br>
    • <b>National Legal Services Authority:</b> nalsa.gov.in | Helpline: 15100<br>
    • <b>Supreme Court Legal Aid:</b> 011-23388922<br>
    • Contact your state High Court for free legal representation
    </div>
    """, unsafe_allow_html=True)