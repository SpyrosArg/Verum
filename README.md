# Verum

> Proof that AI saw what you think it saw.

AI systems are trusted to act on real data. Verum makes that trust verifiable, sealing the data entering an AI system before any processing begins and binding that seal to whatever decision follows. The result is a compact, tamper-evident receipt that anyone can verify, at any time, without access to the AI itself.

```
pip install verum
```

No dependencies. Standard library only. Python 3.9+.

---

## The problem

AI audit systems record what a model decided. They do not record whether the data the model acted on was genuine at the moment of decision.

If input data is altered before it reaches the AI, in transit, at a pipeline handoff, by a compromised agent, the decision log shows nothing wrong. The model made the right call on the wrong data. That gap is unsealed.

Verum seals it.

---

## How it works

```
  raw data arrives
        │
        ▼
  ┌─────────────┐
  │  seal()     │  SHA3-256 fingerprint
  │             │  nanosecond timestamp
  │             │  32-byte nonce
  └──────┬──────┘
         │
         ▼
  AI processes normally
         │
         ▼
  ┌─────────────┐
  │  bind()     │  chains seal → decision hash
  │             │  produces receipt
  └──────┬──────┘
         │
         ▼
  receipt travels with decision
         │
         ▼
  ┌─────────────┐
  │  verify()   │  recomputes fingerprint
  │             │  timing-safe comparison
  │             │  returns VerumResult
  └─────────────┘
```

### seal(data, source_id)

Takes a SHA3-256 fingerprint of the raw input, combined with a nanosecond timestamp and a `secrets.token_hex(16)` nonce. Fields are length-prefixed before hashing to prevent separator collision, `data="a|b", source_id="c"` produces a different fingerprint than `data="a", source_id="b|c"`.

```python
s = seal(data="your raw input data here", source_id="agent-1")
# {
#   "fingerprint": "3a7f...",
#   "source_id":   "agent-1",
#   "timestamp_ns": 1745123456789012345,
#   "nonce":        "8e3c1a...",
#   "version":      "verum-1.0"
# }
```

### bind(seal, decision)

Hashes the AI decision string, then chains `fingerprint | decision_hash` into a single `chain` value. The receipt ties the input proof to the output irrevocably.

```python
receipt = bind(seal=s, decision="ai decision output here")
# {
#   "seal":          { ...seal dict... },
#   "decision_hash": "d4f2...",
#   "chain":         "9b1c...",
#   "bound_at_ns":   1745123456799012345
# }
```

### verify(receipt, original_data)

Recomputes the fingerprint from the claimed original data using the same source_id, timestamp, and nonce stored in the receipt, then compares against the stored fingerprint using `hmac.compare_digest` timing-safe, no early exit. Then independently verifies the chain hash.

```python
result = verify(receipt=receipt, original_data="your raw input data here")

print(result.valid)    # True
print(result.reason)   # "input matches seal, timestamp intact"
print(bool(result))    # True — VerumResult supports bool context
```

If the data was altered:

```python
result = verify(receipt=receipt, original_data="your modified data here")

print(result.valid)    # False
print(result.reason)   # "input does not match seal — data was changed"
```

---

## Full receipt

```python
from verum import seal, bind, verify, export, load

s = seal(data="your raw input data here")
receipt = bind(seal=s, decision="ai decision output here")

print(export(receipt))
```

```json
{
  "seal": {
    "fingerprint": "3a7f4c2e1b9d8a6f0e5c3b1a9f7d4e2c0b8a6f4e2c0b8a6f4e2c0b8a6f4e2c0",
    "source_id": "default",
    "timestamp_ns": 1745123456789012345,
    "nonce": "8e3c1a9f2b4d6e0a1c3f5b7d",
    "version": "verum-1.0"
  },
  "decision_hash": "d4f2c0b8a6e4c2a0f8e6d4c2b0a8f6e4d2c0b8a6f4e2c0b8a6f4e2c0b8a6f4",
  "chain": "9b1c3e5a7d9f1b3e5a7d9f1b3e5a7d9f1b3e5a7d9f1b3e5a7d9f1b3e5a7d9f",
  "bound_at_ns": 1745123456799012345
}
```

Receipts are JSON-serializable. Store them in your audit log, attach them to your decision records, or embed them in your pipeline output. `load()` deserializes them back.

---

## API reference

| Function | Arguments | Returns |
|---|---|---|
| `seal(data, source_id)` | `data: str`, `source_id: str = "default"` | `dict` |
| `bind(seal, decision)` | `seal: dict`, `decision: str` | `dict` |
| `verify(receipt, original_data)` | `receipt: dict`, `original_data: str` | `VerumResult` |
| `export(receipt)` | `receipt: dict` | `str` (JSON) |
| `load(receipt_json)` | `receipt_json: str` | `dict` |
| `VerumMiddleware` | FastAPI/Starlette middleware | auto-seals every request |

### VerumResult

```python
result.valid    # bool
result.reason   # str
bool(result)    # same as result.valid
```

---

## FastAPI middleware

```python
from fastapi import FastAPI
from verum.middleware import VerumMiddleware

app = FastAPI()
app.add_middleware(VerumMiddleware)
```

Every POST request with a body is sealed automatically before any route handler runs. The receipt is available in two places:

- `request.state.verum_seal` —> inside your route handler
- `X-Verum-Fingerprint`, `X-Verum-Chain`, `X-Verum-Source` —> in the response headers

```python
@app.post("/decide")
async def decide(request: Request):
    seal = request.state.verum_seal
    result = run_ai(await request.body())
    receipt = bind(seal=seal, decision=result)
    return {"decision": result, "receipt": export(receipt)}
```

Requires: `pip install verum[fastapi]`

---

## Security properties

- **SHA3-256** —> fingerprint and chain hashes throughout
- **`hmac.compare_digest`** —> timing-safe comparison in verify(), no early exit
- **`secrets.token_hex(16)`** —> cryptographically random nonce, ensures two seals of identical data are always different
- **Length-prefixed encoding** —> prevents separator collision attacks at the fingerprint level
- **No dependencies** —> standard library only, no supply chain surface


---

## Files

```
verum/
├── verum/
│   ├── __init__.py         package exports
│   ├── core.py             the primitive
│   └── middleware.py       FastAPI middleware
├── example.py              three-agent pipeline walkthrough
├── example_space.py        satellite telemetry scenario
└── README.md
```

---

MIT  use it, break it, build on it.
