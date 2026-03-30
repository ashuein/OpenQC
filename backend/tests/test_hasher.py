"""Unit tests for backend.utils.hasher."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest

# Ensure the backend package is importable when running pytest from the repo root.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from backend.utils.hasher import GENESIS_HASH, hash_chain_entry, hash_file, hash_string


class TestHashFile:
    def test_consistent_sha256(self) -> None:
        data = b"hello world"
        expected = hashlib.sha256(data).hexdigest()
        assert hash_file(data) == expected

    def test_empty_bytes(self) -> None:
        expected = hashlib.sha256(b"").hexdigest()
        assert hash_file(b"") == expected


class TestHashString:
    def test_consistent_sha256(self) -> None:
        text = "OpenQC"
        expected = hashlib.sha256(text.encode("utf-8")).hexdigest()
        assert hash_string(text) == expected

    def test_empty_string(self) -> None:
        expected = hashlib.sha256(b"").hexdigest()
        assert hash_string("") == expected


class TestHashChainEntry:
    def test_deterministic(self) -> None:
        payload = "some audit payload"
        prev = GENESIS_HASH
        result1 = hash_chain_entry(payload, prev)
        result2 = hash_chain_entry(payload, prev)
        assert result1 == result2

    def test_matches_manual_computation(self) -> None:
        payload = "entry1"
        prev = GENESIS_HASH
        expected = hashlib.sha256((payload + prev).encode("utf-8")).hexdigest()
        assert hash_chain_entry(payload, prev) == expected


class TestGenesisHash:
    def test_is_64_zeros(self) -> None:
        assert GENESIS_HASH == "0" * 64
        assert len(GENESIS_HASH) == 64
