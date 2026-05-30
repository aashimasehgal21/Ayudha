<div align="center">

<img src="https://img.shields.io/badge/AYUDHA-AI%20Legal%20Assistant-c0392b?style=for-the-badge&labelColor=1a1a2e" />

# 🛡️ AYUDHA
### *AI-Powered Legal Assistance & Support Platform for Women*

> **"Ayudha" (आयुध)** — Sanskrit for *weapon* or *instrument*. This platform is a weapon of knowledge, empowering women to fight for their rights.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.123-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-1.2-1C3C3C?style=flat-square&logo=langchain&logoColor=white)](https://langchain.com/)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-OpenAI-412991?style=flat-square&logo=openai&logoColor=white)](https://openai.com/)
[![Supabase](https://img.shields.io/badge/Supabase-pgvector-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com/)

</div>

---

## 📖 Overview

**Ayudha** is an intelligent, full-stack AI platform built to empower women through accessible legal knowledge and compassionate support. In a country where millions of women are unaware of the rights and protections available to them, Ayudha bridges the gap between complex legal systems and everyday users — no lawyer, no fees, no jargon.

At its core, Ayudha uses **Retrieval-Augmented Generation (RAG)** to ground every legal response in real Indian laws and procedures — not hallucinations. A LangChain-powered agent classifies each query and routes it intelligently: legal questions go through the RAG pipeline, emotional distress triggers the therapy module, voice inputs are transcribed by Whisper, and formal complaints are auto-drafted from structured templates.

Whether a user needs to understand Section 498A, draft an FIR, find a nearby NGO, or simply have someone listen — Ayudha is there, 24/7, in plain language.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🤖 **Legal Chat Assistant** | GPT-4o-mini powered conversational AI grounded in Indian women's rights laws |
| 🎙️ **Voice Chat** | Speak your query — Whisper transcribes, TTS responds back |
| 📄 **Complaint Draft Generator** | Auto-generates formal FIR and complaint letters |
| 🔍 **Evidence Analyzer** | AI reviews submitted evidence and provides legal insights |
| 📅 **Incident Timeline Generator** | Creates structured, date-ordered timelines from user accounts |
| 💜 **Emotional Support Assistant** | Trauma-informed, empathetic AI conversations |
| 🗺️ **NGO Finder** | Locates nearby NGOs and legal aid organizations |
| 📚 **RAG Legal Knowledge Base** | Retrieves precise legal sections from curated Indian law documents |
| 🧠 **Conversation Memory** | Maintains full context across multi-turn conversations |
| 🔐 **Prompt Injection Protection** | Guards against adversarial and harmful prompt attacks |
| 📊 **BLEU & ROUGE Evaluation** | Automated quality measurement of AI responses |
| 🌐 **Sentiment Analysis** | Understands emotional tone to adapt responses accordingly |

---

## 🏗️ Architecture

The platform is structured in four clear layers.

The **Frontend layer** (Streamlit) handles all user-facing interactions across seven specialized pages — legal chat, voice assistant, complaint drafting, evidence analysis, incident timeline, emotional support, and NGO finder.

The **Middleware layer** (FastAPI + LangChain) sits between the UI and the AI services. It applies prompt injection filtering via Prompt Guard, runs NLP sentiment analysis, and uses a query classifier + LangChain agent to determine how each request should be handled.

The **AI Services layer** routes queries to one of two paths: the RAG pipeline, which searches a curated vector database of Indian laws, procedures, and complaint templates stored in Supabase pgvector; or GPT-4o-mini directly, for general legal questions that do not require document retrieval.

The **Data layer** (Supabase) stores the full legal corpus, user data, and session memory — ensuring every conversation is contextually aware and every legal answer is traceable to a real source document.

```
User
 │
 ▼
Frontend Layer — Streamlit
 ├── Legal chat · Voice chat · Complaint draft
 └── Evidence · NGO finder · Timeline · Therapy
 │
 ▼
Middleware — FastAPI + LangChain
 ├── Security filter (Prompt Guard)
 ├── NLP + Sentiment analysis
 ├── Query classifier
 └── LangChain agent
 │
 ▼
AI Services Layer
 ├── RAG Pipeline → laws · procedures · templates
 └── LLM Direct  → GPT-4o-mini · general answers
 │
 ▼
Data Layer — Supabase
 ├── Legal corpus (pgvector)
 ├── User data
 └── Session memory
 │
 ▼
Response delivered to user
```

---

## 📁 Project Structure

```text
AYUDHA/
│
├── app.py                         # Main Streamlit Entry Point
│
├── backend/
│   ├── agent/                     # AI Agent Layer
│   │   ├── agent_core.py
│   │   ├── agent_langchain.py
│   │   ├── agent_prompts.py
│   │   ├── classifier.py
│   │   ├── router.py
│   │   └── test_agent_langchain.py
│   │
│   ├── api/                       # FastAPI Backend
│   │   └── main.py
│   │
│   ├── data/                      # Legal Knowledge Base
│   │   ├── laws/                  # Indian women's rights laws
│   │   ├── procedures/            # Legal procedures
│   │   └── templates/             # Complaint templates
│   │
│   ├── db/                        # Database Layer
│   │   └── supabase_client.py
│   │
│   ├── evaluation/                # Model Evaluation
│   │   ├── evaluate.py
│   │   └── nlp_evaluation.py
│   │
│   ├── memory/                    # Conversation Memory
│   │   ├── conversation_memory.py
│   │   └── test_memory_chat.py
│   │
│   ├── nlp/                       # NLP Processing
│   │   ├── lang_support.py
│   │   └── sentiment.py
│   │
│   ├── rag/                       # RAG Pipeline
│   │   ├── ingest_laws.py
│   │   ├── ingest_procedures.py
│   │   ├── ingest_templates.py
│   │   ├── rag_prompt_builder.py
│   │   ├── rag_search.py
│   │   └── test_rag.py
│   │
│   └── security/
│       └── prompt_guard.py
│
├── pages_app/                     # Streamlit Pages
│   ├── chat.py
│   ├── complaint.py
│   ├── evidence.py
│   ├── ngo.py
│   ├── therapy.py
│   ├── timeline.py
│   └── voice.py
│
├── graphs.py                      # Evaluation Graphs
├── incident_timeline.json
├── evaluation_report.json
├── requirements.txt
└── .env
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Frontend** | Streamlit 1.52 |
| **Backend** | FastAPI + Uvicorn |
| **LLM** | GPT-4o-mini (OpenAI) |
| **Embeddings** | text-embedding-3-small |
| **Speech to Text** | OpenAI Whisper |
| **Text to Speech** | OpenAI TTS |
| **Vector Database** | Supabase pgvector |
| **Relational DB** | PostgreSQL (via Supabase) |
| **AI Framework** | LangChain + LangGraph |
| **NLP** | NLTK |
| **Evaluation** | BLEU + ROUGE scores |
| **Security** | Prompt Guard |
| **Version Control** | Git & GitHub |

---

## 🔐 Security

Ayudha includes a **Prompt Guard** (`backend/security/prompt_guard.py`) that detects and blocks prompt injection attempts, filters harmful or out-of-scope queries, and sanitizes all user inputs before they reach the LLM — applied at the middleware layer on every single request.

---

## 🌍 Pages Overview

| Page | File | Description |
|---|---|---|
| Legal Chat | `pages_app/chat.py` | Main AI legal Q&A interface |
| Voice Assistant | `pages_app/voice.py` | Voice-based legal queries |
| Complaint Drafting | `pages_app/complaint.py` | Generate FIR and complaint letters |
| Evidence Analysis | `pages_app/evidence.py` | Upload and analyze evidence |
| Incident Timeline | `pages_app/timeline.py` | Build a chronological incident timeline |
| Emotional Support | `pages_app/therapy.py` | Empathetic AI counselor |
| NGO Finder | `pages_app/ngo.py` | Find nearby legal aid and NGOs |

---

<div align="center">

*Every woman deserves to know her rights.*
*Ayudha exists so that knowledge is never a barrier.*

**⭐ If this project resonates with you, give it a star — it helps more people find it.**

</div>
