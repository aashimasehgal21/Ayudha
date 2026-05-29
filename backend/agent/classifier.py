# backend/agent/classifier.py

def classify_query(query: str) -> str:
    """
    Strong rule-based classifier for legal queries.

    Returns one of:
    - "LAW"
    - "PROCEDURE"
    - "TEMPLATE"
    - "GENERAL"
    """

    q = query.lower()

   
    #  Detect IPC / Laws / Acts
    
    law_keywords = [
        "ipc", "section", "posh", "pocso", "498a", "354", "376", "509", "law", 
        "indian penal code", "harassment", "molestation", "rape", "stalking",
        "dowry", "domestic violence", "violence act", "legal rights",
        "sexual harassment", "woman safety", "cyber crime", "cybercrime"
    ]

    if any(k in q for k in law_keywords):
        return "LAW"

    # --------------------------
    # 2. Detect procedures (FIR, complaints)
    # --------------------------
    procedure_keywords = [
        "how to file", "fir", "complaint", "file complaint",
        "register case", "police procedure", "investigation",
        "medical examination", "164", "crpc", "charge sheet"
    ]

    if any(k in q for k in procedure_keywords):
        return "PROCEDURE"

    # --------------------------
    # 3. Detect templates
    # --------------------------
    template_keywords = [
        "template", "format", "draft", "letter", "application",
        "sample fir", "sample complaint", "write a complaint"
    ]

    if any(k in q for k in template_keywords):
        return "TEMPLATE"

    # --------------------------
    # 4. If query contains ANY legal signals → treat as LAW
    #    (Safety fallback → ALWAYS give legal help)
    # --------------------------
    safety_signals = [
        "help", "threat", "abuse", "stalking", "harass",
        "unsafe", "violence", "protection", "rights"
    ]

    if any(k in q for k in safety_signals):
        return "LAW"

    # --------------------------
    # 5. Otherwise → GENERAL
    # --------------------------
    return "GENERAL"
