import matplotlib.pyplot as plt

# ====== DATA (replace if needed) ======
# Test scores
test1 = [0.03, 0.54, 0.46]
test2 = [0.05, 0.46, 0.23]

# Average scores
avg = [0.04, 0.50, 0.35]

labels = ['BLEU', 'ROUGE-1', 'ROUGE-L']

# ====== PIE CHART (Average) ======
plt.figure()
plt.pie(avg, labels=labels, autopct='%1.2f')
plt.title("Average NLP Evaluation Scores")

# ====== BAR GRAPH (Comparison) ======
import numpy as np

x = np.arange(len(labels))
width = 0.3

plt.figure()
plt.bar(x - width/2, test1, width, label='Test 1')
plt.bar(x + width/2, test2, width, label='Test 2')

plt.xticks(x, labels)
plt.title("Test 1 vs Test 2 Comparison")
plt.legend()

# ====== SHOW ALL ======
plt.show()