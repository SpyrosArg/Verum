from arche import seal, bind, verify, export

print("=" * 56)
print("  arche — proof that AI saw what you think it saw")
print("=" * 56)

# a three-agent pipeline:
# agent 1 fetches data → agent 2 analyzes → agent 3 decides
# the problem: agent 2 and 3 have no proof agent 1 sent real data

# agent 1 fetches customer data and passes it downstream
data = "customer_id=C9921 credit_score=710 income=52000 debt=8400"

print(f"\n  agent 1 output:  {data}")

# arche seals it at the handoff — before agent 2 touches it
s = seal(data=data, source_id="agent-1-data-fetcher")

print(f"\n  sealed at handoff:  {s['fingerprint'][:36]}...")

# agent 2 analyzes and passes to agent 3
analysis = "risk=low score=0.14 recommendation=approve"
receipt_1 = bind(seal=s, decision=analysis)

print(f"\n  agent 2 analysis:   {analysis}")

# agent 3 makes the final decision
s2 = seal(data=analysis, source_id="agent-2-risk-analyzer")
final = "loan approved — amount 24000 — rate 4.2%"
receipt_2 = bind(seal=s2, decision=final)

print(f"\n  agent 3 decision:   {final}")

# --- verify the full chain ---
print("\n" + "-" * 56)
print("  verifying the full agent chain...")

r1 = verify(receipt=receipt_1, original_data=data)
r2 = verify(receipt=receipt_2, original_data=analysis)

print(f"\n  agent 1 → agent 2:  {r1}")
print(f"  agent 2 → agent 3:  {r2}")

# --- simulate agent 1 being compromised ---
print("\n" + "-" * 56)
print("  scenario: agent 1 was compromised, injected false data")

poisoned = "customer_id=C9921 credit_score=810 income=95000 debt=1200"
print(f"\n  poisoned data:  {poisoned}")

r_poisoned = verify(receipt=receipt_1, original_data=poisoned)
print(f"  chain check:    {r_poisoned}")

print("\n  agent 3 approved the loan based on false input.")
print("  the decision log shows nothing wrong.")
print("  arche exposes the poisoned handoff.")

# --- show receipt ---
print("\n" + "-" * 56)
print("  receipt for agent 1 → agent 2 handoff:\n")
print(export(receipt_1))
print("=" * 56)
