"""Audit trail engine — hash chain operations and verification logic."""

from __future__ import annotations

from backend.utils.hasher import GENESIS_HASH, hash_chain_entry


def compute_entry_hash(
    event_type: str,
    timestamp: str,
    file_name: str | None,
    file_hash: str | None,
    action_detail: str,
    previous_hash: str,
) -> str:
    """Compute the hash for an audit entry.

    Serializes the entry payload deterministically, then chains with previous_hash.
    """
    payload = (
        f"{event_type}|{timestamp}|{file_name or ''}|{file_hash or ''}|{action_detail}"
    )
    return hash_chain_entry(payload, previous_hash)


def verify_chain(entries: list[dict]) -> dict:
    """Verify integrity of audit chain.

    Args:
        entries: list of dicts sorted by sequential ID, each with:
                 id, event_type, timestamp, file_name, file_hash,
                 action_detail, previous_entry_hash, entry_hash

    Returns:
        {"valid": bool, "first_invalid_id": int|None, "entries_checked": int}
    """
    previous_hash = GENESIS_HASH
    for idx, entry in enumerate(entries):
        expected = compute_entry_hash(
            entry["event_type"],
            entry["timestamp"],
            entry.get("file_name"),
            entry.get("file_hash"),
            entry["action_detail"],
            previous_hash,
        )
        if expected != entry["entry_hash"]:
            return {
                "valid": False,
                "first_invalid_id": entry["id"],
                "entries_checked": idx + 1,
            }
        if entry["previous_entry_hash"] != previous_hash:
            return {
                "valid": False,
                "first_invalid_id": entry["id"],
                "entries_checked": idx + 1,
            }
        previous_hash = entry["entry_hash"]
    return {"valid": True, "first_invalid_id": None, "entries_checked": len(entries)}


def verify_file_hash(stored_hash: str, current_hash: str) -> dict:
    """Compare stored file hash with current file hash.

    Returns: {"match": bool, "stored_hash": str, "current_hash": str}
    """
    return {
        "match": stored_hash == current_hash,
        "stored_hash": stored_hash,
        "current_hash": current_hash,
    }
