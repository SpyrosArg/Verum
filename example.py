from arche import seal, bind, verify, export

print("=" * 52)
print("  arche — proof that AI saw what you think it saw")
print("=" * 52)

# the data your AI is about to receive
data = "altitude=408km status=nominal battery=97%"

print(f"\n  input:    {data}")

# seal it before the AI touches it
s = seal(data=data, source_id="satellite-ops-ground-01")
print(f"\n  sealed:   {s['fingerprint'][:32]}...")
print(f"  at:       {s['timestamp_ns']} ns")

# AI makes a decision
decision = "no anomaly detected — system nominal"
receipt = bind(seal=s, decision=decision)

print(f"\n  decision: {decision}")
print(f"  receipt:  {receipt['chain'][:32]}...")

# verify with the original data  passes
print("\n" + "-" * 52)
print("  verifying with original data...")
result = verify(receipt=receipt, original_data=data)
print(f"  {result}")

# now simulate an attacker changing the input
tampered = "altitude=408km status=CRITICAL battery=97%"
print("\n" + "-" * 52)
print("  verifying with tampered data...")
print(f"  tampered: {tampered}")
result = verify(receipt=receipt, original_data=tampered)
print(f"  {result}")

# show the receipt  this is what travels with the decision
print("\n" + "-" * 52)
print("  receipt (travels with the decision):\n")
print(export(receipt))
print("=" * 52)
