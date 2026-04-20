"""
verum — Proof that AI saw what you think it saw.

Three functions:
    seal(data, source_id)           — fingerprint data before AI sees it
    bind(seal, decision)            — attach the seal to an AI decision
    verify(receipt, original_data)  — prove the input was genuine

https://github.com/SpyrosArg/Verum
"""

import hashlib
import hmac
import json
import time
import secrets
from typing import Any


class VerumResult:
    """Result returned by verify(). Check .valid and .reason."""

    def __init__(self, valid: bool, reason: str) -> None:
        self.valid = valid
        self.reason = reason

    def __repr__(self) -> str:
        status = "VALID" if self.valid else "INVALID"
        return f"[{status}] {self.reason}"

    def __bool__(self) -> bool:
        return self.valid


def seal(data: str, source_id: str = "default") -> dict:
    """
    Fingerprint data at the moment it arrives, before any AI touches it.

    Args:
        data:      the raw input string to seal
        source_id: identifier for the data source (e.g. "agent-1", "sensor-feed-03")

    Returns:
        A seal dict. Pass this to bind().
    """
    if not isinstance(data, str):
        raise TypeError(f"data must be a string, got {type(data).__name__}")

    timestamp = time.time_ns()
    nonce = secrets.token_hex(16)

    fingerprint = hashlib.sha3_256(
        f"{data}|{source_id}|{timestamp}|{nonce}".encode("utf-8")
    ).hexdigest()

    return {
        "fingerprint": fingerprint,
        "source_id": source_id,
        "timestamp_ns": timestamp,
        "nonce": nonce,
        "version": "verum-1.0",
    }


def bind(seal: dict, decision: str) -> dict:
    """
    Attach a seal to an AI decision, creating a tamper-evident receipt.

    Args:
        seal:     the dict returned by seal()
        decision: the AI system's output or decision string

    Returns:
        A receipt dict. Store this alongside the decision.
    """
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
    """
    Verify that the original data matches what the AI saw when it decided.

    Args:
        receipt:       the dict returned by bind()
        original_data: the data you believe the AI received

    Returns:
        VerumResult with .valid (bool) and .reason (str).
        Evaluates to True/False in boolean context.
    """
    if not isinstance(original_data, str):
        raise TypeError(f"original_data must be a string, got {type(original_data).__name__}")

    s = receipt["seal"]

    expected = hashlib.sha3_256(
        f"{original_data}|{s['source_id']}|{s['timestamp_ns']}|{s['nonce']}".encode("utf-8")
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
    """Serialize a receipt to a JSON string for storage or transmission."""
    return json.dumps(receipt, indent=2)


def load(receipt_json: str) -> dict:
    """Deserialize a receipt from a JSON string."""
    return json.loads(receipt_json)
