import os
import json
from datetime import datetime
from openai import OpenAI
from backend.agent.agent_core import agent_answer

# Load env
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# TEST DATA
# -------------------------------
TEST_DATA = [
    {
        "question": "What is IPC Section 498A?",
        "expected_keywords": ["cruelty", "husband", "imprisonment", "dowry"],
        "category": "LAW"
    },
    {
        "question": "How to file an FIR for harassment?",
        "expected_keywords": ["police", "complaint", "register", "station"],
        "category": "PROCEDURE"
    },
    {
        "question": "What is the POSH Act?",
        "expected_keywords": ["workplace", "harassment", "committee", "ICC"],
        "category": "LAW"
    },
    {
        "question": "Give me a sample complaint letter for stalking",
        "expected_keywords": ["complaint", "stalking", "police", "section"],
        "category": "TEMPLATE"
    },
    {
        "question": "What is IPC 354?",
        "expected_keywords": ["assault", "modesty", "woman", "imprisonment"],
        "category": "LAW"
    },
    {
        "question": "How to get a protection order under domestic violence act?",
        "expected_keywords": ["protection", "order", "court", "magistrate"],
        "category": "PROCEDURE"
    },
    {
        "question": "Hello how are you?",
        "expected_keywords": ["hello", "help", "assist", "hi"],
        "category": "GENERAL"
    },
    {
        "question": "What is POCSO Act?",
        "expected_keywords": ["child", "sexual", "offence", "protection"],
        "category": "LAW"
    },
    {
        "question": "What is IPC 354 assault on modesty?",
        "expected_keywords": ["assault", "modesty", "woman", "imprisonment"],
        "category": "LAW"
    },
    {
        "question": "What are my rights if police refuse to file FIR?",
        "expected_keywords": ["magistrate", "complaint", "section 156", "refuse"],
        "category": "PROCEDURE"
    },
]

# -------------------------------
# METRICS
# -------------------------------
def score_keyword_match(answer: str, keywords: list) -> float:
    answer_lower = answer.lower()
    matched = sum(1 for kw in keywords if kw.lower() in answer_lower)
    return matched / len(keywords) if keywords else 0.0


def score_llm(prompt: str) -> float:
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        score = float(res.choices[0].message.content.strip())
        return min(max(score, 0.0), 1.0)
    except:
        return 0.5


def score_faithfulness(q, a):
    prompt = f"Rate faithfulness 0-1.\nQ:{q}\nA:{a}"
    return score_llm(prompt)


def score_relevance(q, a):
    prompt = f"Rate relevance 0-1.\nQ:{q}\nA:{a}"
    return score_llm(prompt)


def score_completeness(q, a):
    prompt = f"Rate completeness 0-1.\nQ:{q}\nA:{a}"
    return score_llm(prompt)


# -------------------------------
# PRF FUNCTION
# -------------------------------
def compute_prf(answers, test_data):
    total_tp, total_fp, total_fn = 0, 0, 0

    for item, answer in zip(test_data, answers):
        expected = set(k.lower() for k in item["expected_keywords"])
        answer_words = set(answer.lower().split())

        tp = len(expected & answer_words)
        fn = len(expected - answer_words)
        fp = len(answer_words - expected)

        total_tp += tp
        total_fn += fn
        total_fp += fp

    precision = total_tp / (total_tp + total_fp) if (total_tp + total_fp) else 0
    recall    = total_tp / (total_tp + total_fn) if (total_tp + total_fn) else 0
    f1        = (2 * precision * recall) / (precision + recall) if (precision + recall) else 0

    return round(precision,2), round(recall,2), round(f1,2)


# -------------------------------
# MAIN EVALUATION
# -------------------------------
def evaluate():
    print("\n===== EVALUATION =====\n")

    all_answers = []

    total_kw = total_faith = total_rel = total_comp = 0
    keyword_passes = 0

    for i, item in enumerate(TEST_DATA, 1):
        q = item["question"]
        keywords = item["expected_keywords"]

        try:
            answer = agent_answer(q)
        except:
            answer = "fallback answer"

        all_answers.append(answer)

        kw = score_keyword_match(answer, keywords)
        faith = score_faithfulness(q, answer)
        rel = score_relevance(q, answer)
        comp = score_completeness(q, answer)

        if kw >= 0.5:
            keyword_passes += 1

        total_kw += kw
        total_faith += faith
        total_rel += rel
        total_comp += comp

        print(f"\nQ{i}: {q}")
        print("KW:", kw, "Faith:", faith, "Rel:", rel, "Comp:", comp)

    n = len(TEST_DATA)

    print("\n===== FINAL =====")
    print("Keyword Accuracy:", (keyword_passes/n)*100)

    # 🔥 PRF
    precision, recall, f1 = compute_prf(all_answers, TEST_DATA)

    print("\nPrecision:", precision)
    print("Recall:", recall)
    print("F1:", f1)


# -------------------------------
if __name__ == "__main__":
    evaluate()