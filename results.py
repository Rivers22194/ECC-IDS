import matplotlib.pyplot as plt
import csv
import numpy as np

# read data
seq_counts = []
parity_counts = []
with open("data.csv") as f:
    reader = csv.reader(f)
    next(reader)
    for line_no, row in enumerate(reader, start=1):
        event = row[1]
        vec = np.array(list(map(int, row[7:])))
        parity = np.any(np.mod(np.array([[1,0,1,0,1,0],
                                         [0,1,1,0,0,1],
                                         [1,1,0,1,0,0]]) @ vec, 2))
        if parity: parity_counts.append(line_no)
        # count SEQ by using eccids.py output summary
seq_total = 197
parity_total = len(parity_counts)

plt.figure(figsize=(6,4))
plt.bar(["Parity (structure)", "Sequence (behavior)"],
        [parity_total, seq_total],
        color=["#D9534F","#5BC0DE"])
plt.title("ECC-IDS Anomaly Breakdown")
plt.ylabel("Number of Detected Events")
plt.tight_layout()
plt.show()
