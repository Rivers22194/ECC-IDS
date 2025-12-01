import random
import csv
import numpy as np

# --- Settings ---
NUM_RECORDS = 200       # total rows
ANOMALY_RATE = 0.15     # 15% anomalies
OUT_FILE = "data.csv"

# --- Event grammar ---
NORMAL_SEQ = [["A", random.choice(["C", "D"]), "E"] for _ in range(30)]
ALL_EVENTS = ["A", "B", "C", "D", "E"]

def random_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))

def random_protocol():
    return random.choice(["TCP", "UDP"])

def random_port(proto):
    return random.choice([80, 443, 22, 25, 53, 21]) if proto == "TCP" else random.choice([53, 67, 68, 161])

def random_vec(valid=True):
    """Generate a 6-bit vector; if valid=True, satisfies H×z=0."""
    H = np.array([
        [1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0]
    ], dtype=int)

    while True:
        z = np.random.randint(0, 2, 6)
        if valid and np.all((H @ z) % 2 == 0):
            return z
        if not valid and not np.all((H @ z) % 2 == 0):
            return z

def generate_session(valid=True):
    """Generate a short normal session or an anomalous one."""
    proto = random_protocol()
    src = random_ip()
    dst = random_ip()
    base_port = random_port(proto)

    # Choose a sequence — sometimes break it
    seq = random.choice(NORMAL_SEQ)
    if not valid and random.random() < 0.5:
        seq = random.sample(ALL_EVENTS, 3)  # scrambled order

    rows = []
    for e in seq:
        anomaly_vec = not valid and random.random() < 0.3
        vec = random_vec(valid=not anomaly_vec)
        size = random.randint(200, 900)
        rows.append({
            "event": e,
            "src_ip": src,
            "dst_ip": dst,
            "protocol": proto,
            "port": base_port,
            "size": size,
            "vec": " ".join(map(str, vec))
        })
    return rows

def generate_dataset():
    rows = []
    while len(rows) < NUM_RECORDS:
        valid = random.random() > ANOMALY_RATE
        session = generate_session(valid)
        rows.extend(session)
    return rows[:NUM_RECORDS]

def save_dataset(rows, filename=OUT_FILE):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id","event","src_ip","dst_ip","protocol","port","size","a1","a2","a3","a4","a5","a6"])
        for i, r in enumerate(rows, start=1):
            a1,a2,a3,a4,a5,a6 = map(int, r["vec"].split())
            writer.writerow([i, r["event"], r["src_ip"], r["dst_ip"], r["protocol"], r["port"], r["size"], a1,a2,a3,a4,a5,a6])

if __name__ == "__main__":
    data = generate_dataset()
    save_dataset(data)
    print(f"✅ Generated {len(data)} records → saved to {OUT_FILE}")
    print("   Contains both normal and anomalous traffic samples.")
