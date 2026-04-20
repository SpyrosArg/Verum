# arche

**Proof that AI saw what you think it saw.**

---

Every AI audit system today records what the AI decided.  
Nobody records what the AI actually saw before it decided.

That gap is the problem arche solves.

---

## The problem

```
Real world data  ──────────────────────────>  AI  ──>  Decision  ──>  Signed log ✓
                          ↑
                  manipulated here?
                  nobody proves this
```

Logs prove the decision happened. They cannot prove the input was genuine.  
An attacker who manipulates data *before* the AI sees it leaves no trace in any existing system.

---

## What arche does

```
Data arrives  ──>  arche seals it  ──>  AI decides  ──>  Decision + seal travel together
                   (hash + timestamp)                      Anyone can verify. Anytime.
```

One seal. Travels with the decision. Verifiable by anyone with no access to the AI system itself.  
If the input was manipulated, the seal breaks. Always.

---

## Install

```bash
# no dependencies — standard library only
git clone https://github.com/yourusername/arche.git
```

---

## Usage

```python
from arche import seal, bind, verify

# before the AI sees anything
s = seal(data="telemetry reading: altitude=408km, status=nominal")

# after the AI decides
receipt = bind(seal=s, decision="no anomaly detected")

# anyone verifies — a minute later, a year later, in court
result = verify(receipt=receipt, original_data="telemetry reading: altitude=408km, status=nominal")

print(result.valid)   # True
print(result.reason)  # "input matches seal, timestamp intact"
```

If the data was changed before the AI saw it — `result.valid` is `False`.  
No false negatives. No configuration. No dependencies.

---

## How it works

arche takes a cryptographic fingerprint of the raw input at the moment it arrives — before any AI system touches it. That fingerprint is sealed with an external timestamp the operator does not control. The seal travels inseparably with every decision the AI makes. Anyone can recompute the fingerprint from the original data and check it against the seal. A match means the data was genuine. A mismatch means it was not.

Three functions. Under 150 lines of Python.

---

## Where it applies

- **Space operations** — prove the telemetry an AI anomaly detector acted on was not spoofed
- **Healthcare** — prove the scan an AI diagnostic tool saw was the correct unaltered patient data
- **Finance** — prove the market feed an AI trading system acted on was genuine at that moment
- **AI agent pipelines** — seal every handoff between agents so the full chain is auditable

---

## What arche is not

Not an encryption tool. Not an audit log. Not a compliance framework.  
It is one primitive that fills one gap. Build the rest on top.

---

## Files

```
arche/
├── arche.py           the primitive (~150 lines, no dependencies)
├── example.py         basic demo, runs in 5 seconds
├── example_space.py   satellite telemetry scenario
└── README.md
```

---

MIT License — use it, build on it, propose changes.
