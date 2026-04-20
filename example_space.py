from verum import seal, bind, verify, export
import json

print("=" * 60)
print("  verum — satellite telemetry integrity demo")
print("  scenario: ground station AI anomaly detector")
print("=" * 60)

# a realistic telemetry packet from a satellite
# this is what the ground station AI receives every pass
telemetry = json.dumps({
    "satellite_id": "SAT-EU-07",
    "pass_window": "2026-04-20T03:14:00Z",
    "orbital_altitude_km": 408.3,
    "battery_level_pct": 94.2,
    "attitude_status": "nominal",
    "thermal_temp_c": 21.4,
    "downlink_signal_db": -87.3
})

print(f"\n  satellite:  SAT-EU-07")
print(f"  pass window: 2026-04-20T03:14:00Z")
print(f"  ground station: GSTATION-LUX-01")

# seal the telemetry the moment it arrives
# before the AI anomaly detector processes it
s = seal(data=telemetry, source_id="GSTATION-LUX-01")

print(f"\n  telemetry sealed before AI processing")
print(f"  fingerprint: {s['fingerprint'][:40]}...")

# AI anomaly detector makes its assessment
ai_decision = json.dumps({
    "assessment": "nominal",
    "confidence": 0.97,
    "flags": [],
    "recommended_action": "none"
})

receipt = bind(seal=s, decision=ai_decision)

print(f"\n  AI assessment: nominal — no anomaly detected")
print(f"  receipt bound: {receipt['chain'][:40]}...")

# --- scenario 1: legitimate verification ---
print("\n" + "-" * 60)
print("  SCENARIO 1 — regulator verifies the receipt next month")
print("-" * 60)

result = verify(receipt=receipt, original_data=telemetry)
print(f"  result: {result}")

# --- scenario 2: attacker spoofed the telemetry ---
# but also changed the altitude slightly to mask a maneuver
print("\n" + "-" * 60)
print("  SCENARIO 2 — attacker spoofed altitude before AI saw it")
print("-" * 60)

spoofed_telemetry = json.dumps({
    "satellite_id": "SAT-EU-07",
    "pass_window": "2026-04-20T03:14:00Z",
    "orbital_altitude_km": 412.1,   # changed — masked maneuver
    "battery_level_pct": 94.2,
    "attitude_status": "nominal",
    "thermal_temp_c": 21.4,
    "downlink_signal_db": -87.3
})

print(f"  real altitude:    408.3 km")
print(f"  spoofed altitude: 412.1 km")
print(f"  AI saw the spoofed value and said: nominal")
print(f"  but the seal was taken on the real feed...")

result = verify(receipt=receipt, original_data=spoofed_telemetry)
print(f"  result: {result}")

print("\n  the seal exposes the manipulation.")
print("  the AI decision log shows nothing wrong.")
print("  verum catches what the log cannot.")

# --- show the receipt ---
print("\n" + "-" * 60)
print("  full receipt — travels with every AI decision:")
print("-" * 60)
print(export(receipt))
print("=" * 60)
