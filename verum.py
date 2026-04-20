
import hashlib
import hmac
import json
import time
import secrets


def seal(data: str, source_id: str = "default") -> dict:
    timestamp = time.time_ns()
    nonce = secrets.token_hex(16)
    
    fingerprint = hashlib.sha3_256(
        f"{data}|{source_id}|{timestamp}|{nonce}".encode()
    ).hexdigest()

    return {
        "fingerprint": fingerprint,
        "source_id": source_id,
        "timestamp_ns": timestamp,
        "nonce": nonce,
        "version": "verum-1.0"
    }


def bind(seal: dict, decision: str) -> dict:
    decision_hash = hashlib.sha3_256(decision.encode()).hexdigest()

    chain = hashlib.sha3_256(
        f"{seal['fingerprint']}|{decision_hash}".encode()
    ).hexdigest()

    return {
        "seal": seal,
        "decision_hash": decision_hash,
        "chain": chain,
        "bound_at_ns": time.time_ns()
    }


def verify(receipt: dict, original_data: str) -> object:

    class Result:
        def __init__(self, valid, reason):
            self.valid = valid
            self.reason = reason
        def __repr__(self):
            status = "VALID" if self.valid else "INVALID"
            return f"[{status}] {self.reason}"

    s = receipt["seal"]

    expected = hashlib.sha3_256(
        f"{original_data}|{s['source_id']}|{s['timestamp_ns']}|{s['nonce']}".encode()
    ).hexdigest()

    if not hmac.compare_digest(expected, s["fingerprint"]):
        return Result(False, "input does not match seal — data was changed")

    expected_chain = hashlib.sha3_256(
        f"{s['fingerprint']}|{receipt['decision_hash']}".encode()
    ).hexdigest()

    if not hmac.compare_digest(expected_chain, receipt["chain"]):
        return Result(False, "chain broken — receipt was tampered with")

    return Result(True, "input matches seal, timestamp intact")


def export(receipt: dict) -> str:
    return json.dumps(receipt, indent=2)


def load(receipt_json: str) -> dict:
    return json.loads(receipt_json)
