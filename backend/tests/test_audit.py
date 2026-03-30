"""Unit tests for the audit trail engine (backend.engine.audit_engine)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.engine.audit_engine import compute_entry_hash, verify_chain, verify_file_hash
from backend.utils.hasher import GENESIS_HASH


# ---------------------------------------------------------------------------
# Helper to build a valid chain of entry dicts
# ---------------------------------------------------------------------------

def _build_chain(count: int) -> list[dict]:
    """Build a list of *count* valid chained entry dicts."""
    entries: list[dict] = []
    previous_hash = GENESIS_HASH
    for i in range(1, count + 1):
        ts = f"2025-01-01T00:00:0{i}"
        event_type = "upload"
        file_name = f"file_{i}.csv"
        file_hash = f"{'a' * 63}{i}"
        action_detail = f"Uploaded file_{i}.csv"
        entry_hash = compute_entry_hash(
            event_type, ts, file_name, file_hash, action_detail, previous_hash,
        )
        entries.append(
            {
                "id": i,
                "event_type": event_type,
                "timestamp": ts,
                "file_name": file_name,
                "file_hash": file_hash,
                "action_detail": action_detail,
                "previous_entry_hash": previous_hash,
                "entry_hash": entry_hash,
            }
        )
        previous_hash = entry_hash
    return entries


# ---------------------------------------------------------------------------
# Tests for compute_entry_hash
# ---------------------------------------------------------------------------

class TestComputeEntryHash:
    def test_deterministic(self) -> None:
        """Same inputs must always produce the same hash."""
        args = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        assert compute_entry_hash(*args) == compute_entry_hash(*args)

    def test_changes_with_event_type(self) -> None:
        base = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        altered = ("view", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        assert compute_entry_hash(*base) != compute_entry_hash(*altered)

    def test_changes_with_timestamp(self) -> None:
        base = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        altered = ("upload", "2025-01-02T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        assert compute_entry_hash(*base) != compute_entry_hash(*altered)

    def test_changes_with_file_name(self) -> None:
        base = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        altered = ("upload", "2025-01-01T00:00:00", "other.csv", "abc123", "File uploaded", GENESIS_HASH)
        assert compute_entry_hash(*base) != compute_entry_hash(*altered)

    def test_changes_with_file_hash(self) -> None:
        base = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        altered = ("upload", "2025-01-01T00:00:00", "report.csv", "def456", "File uploaded", GENESIS_HASH)
        assert compute_entry_hash(*base) != compute_entry_hash(*altered)

    def test_changes_with_action_detail(self) -> None:
        base = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        altered = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File deleted", GENESIS_HASH)
        assert compute_entry_hash(*base) != compute_entry_hash(*altered)

    def test_changes_with_previous_hash(self) -> None:
        base = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", GENESIS_HASH)
        altered = ("upload", "2025-01-01T00:00:00", "report.csv", "abc123", "File uploaded", "f" * 64)
        assert compute_entry_hash(*base) != compute_entry_hash(*altered)

    def test_nullable_fields(self) -> None:
        """None for file_name and file_hash should serialize as empty string."""
        h = compute_entry_hash("settings", "2025-01-01T00:00:00", None, None, "Changed setting", GENESIS_HASH)
        assert isinstance(h, str) and len(h) == 64


# ---------------------------------------------------------------------------
# Tests for verify_chain
# ---------------------------------------------------------------------------

class TestVerifyChain:
    def test_valid_chain_three_entries(self) -> None:
        entries = _build_chain(3)
        result = verify_chain(entries)
        assert result["valid"] is True
        assert result["first_invalid_id"] is None
        assert result["entries_checked"] == 3

    def test_tampered_entry_hash(self) -> None:
        entries = _build_chain(3)
        # Tamper with the second entry's hash
        entries[1]["entry_hash"] = "bad_hash_" + "0" * 55
        result = verify_chain(entries)
        assert result["valid"] is False
        assert result["first_invalid_id"] == 2
        assert result["entries_checked"] == 2

    def test_tampered_previous_entry_hash(self) -> None:
        entries = _build_chain(3)
        # Tamper with the third entry's previous_entry_hash
        entries[2]["previous_entry_hash"] = "bad_prev_" + "0" * 55
        result = verify_chain(entries)
        assert result["valid"] is False
        assert result["first_invalid_id"] == 3
        assert result["entries_checked"] == 3

    def test_empty_list(self) -> None:
        result = verify_chain([])
        assert result["valid"] is True
        assert result["first_invalid_id"] is None
        assert result["entries_checked"] == 0

    def test_single_valid_entry(self) -> None:
        entries = _build_chain(1)
        result = verify_chain(entries)
        assert result["valid"] is True
        assert result["entries_checked"] == 1


# ---------------------------------------------------------------------------
# Tests for verify_file_hash
# ---------------------------------------------------------------------------

class TestVerifyFileHash:
    def test_match(self) -> None:
        result = verify_file_hash("abc123", "abc123")
        assert result["match"] is True
        assert result["stored_hash"] == "abc123"
        assert result["current_hash"] == "abc123"

    def test_mismatch(self) -> None:
        result = verify_file_hash("abc123", "def456")
        assert result["match"] is False
        assert result["stored_hash"] == "abc123"
        assert result["current_hash"] == "def456"


# ---------------------------------------------------------------------------
# Tests for chain linking / GENESIS_HASH usage
# ---------------------------------------------------------------------------

class TestChainLinking:
    def test_first_entry_uses_genesis_hash(self) -> None:
        entries = _build_chain(1)
        assert entries[0]["previous_entry_hash"] == GENESIS_HASH

    def test_chain_links_previous_hash(self) -> None:
        entries = _build_chain(3)
        assert entries[1]["previous_entry_hash"] == entries[0]["entry_hash"]
        assert entries[2]["previous_entry_hash"] == entries[1]["entry_hash"]
