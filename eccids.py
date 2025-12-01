import numpy as np, csv
from collections import Counter

H=np.array([
    [1,0,1,0,1,0],
    [0,1,1,0,0,1],
    [1,1,0,1,0,0]
],dtype=int)

def syndrome(z): return (H@z)%2
def is_valid(z): return np.all(syndrome(z)==0)

DFA={
    "START":{"A":"LOGIN"},
    "LOGIN":{"C":"TRANSFER","D":"TRANSFER"},
    "TRANSFER":{"E":"LOGOUT"},
    "LOGOUT":{}
}
def legal(state,sym): return sym in DFA.get(state,{})

# --- read dataset ---
records=[]
with open("data.csv") as f:
    r=csv.reader(f); next(r)
    for row in r:
        if not row: continue
        e=row[1]; meta=row[2:7]; z=np.array(list(map(int,row[7:])))
        records.append((e,meta,z))

# --- run detection ---
counts=Counter(); state="START"
print(f"{'Line':<5}{'Evt':<4}{'Src→Dst':<25}{'Proto':<6}{'Sz':<6}Status")
print("-"*70)
for i,(e,meta,z) in enumerate(records,1):
    src,dst,p,port,sz=meta
    ok1=is_valid(z)
    ok2=legal(state,e)
    if not ok1 or not ok2:
        reason=[]
        if not ok1: reason.append("PARITY")
        if not ok2: reason.append("SEQ")
        counts.update(reason)
        print(f"{i:<5}{e:<4}{src+'→'+dst:<25}{p:<6}{sz:<6}{','.join(reason)}")
    else:
        state=DFA[state][e]

print("\nSummary:",dict(counts))
print(f"Total {len(records)} entries checked.")
print("\nInterpretation:")
if counts:
    if counts['PARITY']:
        print(f"• {counts['PARITY']} parity anomalies → structural corruption or tampering.")
    if counts['SEQ']:
        print(f"• {counts['SEQ']} sequence anomalies → misordered or suspicious activity.")
else:
    print("No anomalies: traffic is clean.")
