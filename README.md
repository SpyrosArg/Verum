# Verum

> *Proof that AI saw what you think it saw.*

&nbsp;

Every tool in the AI audit space records what the model **decided**.  
No tool records whether the data the model saw was **real**.

That is the gap. verum closes it.

&nbsp;

## The gap nobody is talking about

```mermaid
flowchart TD
    A(["Real world data
    ───────────────
    telemetry · sensors · feeds"])

    B(["Silent manipulation
    ───────────────
    possible here · undetectable
    no tool catches this"])

    C(["AI system
    ───────────────
    processes what it receives"])

    D(["Decision
    ───────────────
    signed and logged ✓"])

    A -->|enters pipeline| B
    B -->|reaches AI unchallenged| C
    C --> D

    style A fill:#f8fafc,stroke:#94a3b8,color:#334155
    style B fill:#fff1f2,stroke:#fda4af,color:#9f1239
    style C fill:#f8fafc,stroke:#94a3b8,color:#334155
    style D fill:#f0fdf4,stroke:#86efac,color:#166534
```

Logs prove the decision happened.  
They cannot prove the input was genuine.

&nbsp;

## What verum does

```mermaid
flowchart TD
    A(["Data arrives
    ───────────────
    raw · untouched · live"])

    B(["verum seals it
    ───────────────
    fingerprint + timestamp
    before AI sees anything"])

    C(["AI processes
    ───────────────
    works as normal
    nothing changes"])

    D(["Receipt is born
    ───────────────
    decision + seal together
    compact · tamper-evident"])

    E(["Anyone verifies
    ───────────────
    regulator · court · auditor
    no AI access needed"])

    A --> B
    B --> C
    C --> D
    D --> E

    style A fill:#f8fafc,stroke:#94a3b8,color:#334155
    style B fill:#eff6ff,stroke:#93c5fd,color:#1e40af
    style C fill:#f8fafc,stroke:#94a3b8,color:#334155
    style D fill:#eff6ff,stroke:#93c5fd,color:#1e40af
    style E fill:#f0fdf4,stroke:#86efac,color:#166634
```

One seal. Generated before the AI touches anything.  
If the input was changed, the seal breaks. Always.

&nbsp;

## Get started

No pip. No dependencies. Clone and run.

```bash
git clone https://github.com/SpyrosArg/Verum.git
python example.py
```

&nbsp;

## Three functions

```python
from verum import seal, bind, verify

# before the AI sees anything
s = seal(data="your raw input data here")

# after the AI decides
receipt = bind(seal=s, decision="ai decision output here")

# verify anytime — by anyone
result = verify(receipt=receipt, original_data="your raw input data here")

print(result.valid)    # True
print(result.reason)   # "input matches seal"
```

Change a single character in the original data. `result.valid` becomes `False`.  
That is the entire interface.

&nbsp;

## Where this matters

**AI agent pipelines**  
One agent feeds another. Seal every handoff. Make the entire chain auditable at every link.

**Space operations**  
The telemetry an AI anomaly detector acted on —> was it real? Prove it.

**Healthcare**  
The scan an AI diagnostic tool processed —> was it the right patient, unaltered? Prove it.

**Finance**  
The market data an algorithmic system acted on —> was it the genuine feed at that moment? Prove it.



&nbsp;

## How it works

verum takes a cryptographic fingerprint of raw input the moment it arrives. It seals that fingerprint with a timestamp from an external source the operator does not control, so nothing can be backdated. The seal binds to whatever decision follows. Verification reruns the fingerprint on the original data and checks it against the seal. Match means genuine. Mismatch means something changed.


&nbsp;

## What this is not

Not encryption. Not an audit log. Not a compliance platform.  
One primitive. One gap. Everything else builds on top.

&nbsp;

```
verum/
├── verum.py            the primitive
├── example.py          start here
├── example_space.py    satellite telemetry walkthrough
└── README.md
```

&nbsp;

MIT  use it, break it, build on it.
