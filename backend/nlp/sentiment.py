# backend/nlp/sentiment.py

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SENTIMENT_PROMPT = """
You are analyzing a message from a woman who may be in distress or seeking legal help.

Analyze the message and return ONLY a valid JSON object with these exact fields:
- sentiment: one of "distressed" | "angry" | "scared" | "neutral" | "seeking_info"
- urgency: one of "high" | "medium" | "low"
- needs_empathy: true or false
- is_emergency: true or false (only true if she mentions immediate physical danger)
- language: one of "hindi" | "english" | "hinglish"

Message: {text}

Return ONLY the JSON. No explanation. No extra text.
"""

def analyze_sentiment(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": SENTIMENT_PROMPT.format(text=text)
            }],
            temperature=0
        )
        raw = response.choices[0].message.content.strip()
        # strip markdown if model wraps in ```json
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return json.loads(raw.strip())
    except Exception as e:
        print(f"[Sentiment Error] {e}")
        return {
            "sentiment": "neutral",
            "urgency": "low",
            "needs_empathy": False,
            "is_emergency": False,
            "language": "english"
        }