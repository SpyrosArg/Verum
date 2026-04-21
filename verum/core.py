import hashlib
import hmac
import json
import secrets
import time


class VerumResult:

    def __init__(self, valid: bool, reason: str) -> None:
        self.valid = valid
        self.reason = reason

    def __repr__(self) -> str:
        status = "VALID" if self.valid else "INVALID"
        return f"[{status}] {self.reason}"

    def __bool__(self) -> bool:
        return self.valid


def _encode(data: str, source_id: str, timestamp: int, nonce: str) -> bytes:
    parts = f"{len(data)}:{data}|{len(source_id)}:{source_id}|{timestamp}|{nonce}"
    return parts.encode("utf-8")


def seal(data: str, source_id: str = "default") -> dict:
    if not isinstance(data, str):
        raise TypeError(f"data must be a string, got {type(data).__name__}")

    timestamp = time.time_ns()
    nonce = secrets.token_hex(16)

    fingerprint = hashlib.sha3_256(
        _encode(data, source_id, timestamp, nonce)
    ).hexdigest()

    return {
        "fingerprint": fingerprint,
        "source_id": source_id,
        "timestamp_ns": timestamp,
        "nonce": nonce,
        "version": "verum-1.0",
    }


def bind(seal: dict, decision: str) -> dict:
    if not isinstance(decision, str):
        raise TypeError(f"decision must be a string, got {type(decision).__name__}")

    decision_hash = hashlib.sha3_256(decision.encode("utf-8")).hexdigest()

    chain = hashlib.sha3_256(
        f"{seal['fingerprint']}|{decision_hash}".encode("utf-8")
    ).hexdigest()

    return {
        "seal": seal,
        "decision_hash": decision_hash,
        "chain": chain,
        "bound_at_ns": time.time_ns(),
    }


def verify(receipt: dict, original_data: str) -> VerumResult:
    if not isinstance(original_data, str):
        raise TypeError(f"original_data must be a string, got {type(original_data).__name__}")

    s = receipt["seal"]

    expected = hashlib.sha3_256(
        _encode(original_data, s["source_id"], s["timestamp_ns"], s["nonce"])
    ).hexdigest()

    if not hmac.compare_digest(expected, s["fingerprint"]):
        return VerumResult(False, "input does not match seal — data was changed")

    expected_chain = hashlib.sha3_256(
        f"{s['fingerprint']}|{receipt['decision_hash']}".encode("utf-8")
    ).hexdigest()

    if not hmac.compare_digest(expected_chain, receipt["chain"]):
        return VerumResult(False, "chain broken — receipt was tampered with")

    return VerumResult(True, "input matches seal, timestamp intact")


def export(receipt: dict) -> str:
    return json.dumps(receipt, indent=2)


def load(receipt_json: str) -> dict:
    return json.loads(receipt_json)
