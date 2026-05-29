# backend/evaluation/nlp_evaluation.py

import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

# Download once
nltk.download('punkt')

# ---------------- SAMPLE DATA ----------------
# Replace with your actual queries

test_data = [
    {
        "reference": "IPC 354 deals with assault on a woman's modesty and provides punishment.",
        "prediction": "Section 354 IPC covers assault or criminal force against a woman and punishment."
    },
    {
        "reference": "You can file an FIR at the nearest police station for harassment.",
        "prediction": "To report harassment, you should go to a police station and register an FIR."
    }
]

# ---------------- BLEU SCORE ----------------
def compute_bleu(reference, prediction):
    ref_tokens = [reference.split()]
    pred_tokens = prediction.split()

    smoothie = SmoothingFunction().method4
    score = sentence_bleu(ref_tokens, pred_tokens, smoothing_function=smoothie)
    return score


# ---------------- ROUGE SCORE ----------------
def compute_rouge(reference, prediction):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, prediction)

    return {
        "rouge1": scores["rouge1"].fmeasure,
        "rougeL": scores["rougeL"].fmeasure
    }


# ---------------- MAIN EVALUATION ----------------
def evaluate():
    print("\n🔍 NLP Evaluation (BLEU & ROUGE)\n")

    total_bleu = 0
    total_r1 = 0
    total_rL = 0

    for i, item in enumerate(test_data, 1):
        ref = item["reference"]
        pred = item["prediction"]

        bleu = compute_bleu(ref, pred)
        rouge = compute_rouge(ref, pred)

        total_bleu += bleu
        total_r1 += rouge["rouge1"]
        total_rL += rouge["rougeL"]

        print(f"Test {i}")
        print(f"BLEU Score  : {bleu:.2f}")
        print(f"ROUGE-1     : {rouge['rouge1']:.2f}")
        print(f"ROUGE-L     : {rouge['rougeL']:.2f}")
        print("-" * 40)

    n = len(test_data)

    print("\n📊 FINAL SCORES")
    print(f"Average BLEU   : {total_bleu/n:.2f}")
    print(f"Average ROUGE-1: {total_r1/n:.2f}")
    print(f"Average ROUGE-L: {total_rL/n:.2f}")


if __name__ == "__main__":
    evaluate()