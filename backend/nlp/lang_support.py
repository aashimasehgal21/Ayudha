# backend/nlp/lang_support.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DETECT_PROMPT = """
Detect the language of this text. Reply with ONLY one word:
- hindi (if written in Devanagari script)
- hinglish (if Hindi words written in English letters like "mujhe madad chahiye")
- english (if pure English)

Text: {text}
"""

TRANSLATE_PROMPT = """
You are a helpful translator.
Translate this English legal response into {lang} language.
If lang is "hinglish", write in Hindi but using English letters (Roman script).
If lang is "hindi", write in Devanagari script.
Keep legal terms like IPC, FIR, POSH in English.
Keep the meaning exact — do not add or remove information.

English text:
{text}

Translated response:
"""

def detect_language(text: str) -> str:
    """Returns: 'hindi', 'hinglish', or 'english'"""
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": DETECT_PROMPT.format(text=text)
            }],
            temperature=0
        )
        lang = res.choices[0].message.content.strip().lower()
        if lang in ["hindi", "hinglish", "english"]:
            return lang
        return "english"
    except Exception as e:
        print(f"[Lang detect error] {e}")
        return "english"

def translate_response(text: str, lang: str) -> str:
    """Translate English response to target language"""
    if lang == "english":
        return text
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": TRANSLATE_PROMPT.format(lang=lang, text=text)
            }],
            temperature=0.3
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Translate error] {e}")
        return text

def process_with_lang(query: str, answer: str) -> str:
    """Detect query language, translate answer if needed"""
    lang = detect_language(query)
    print(f"[Lang] Detected: {lang}")
    if lang == "english":
        return answer
    return translate_response(answer, lang)