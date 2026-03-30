"""
Cryptographic hashing utilities for file integrity and audit chain.

All functions use SHA-256 and are pure / deterministic.
"""

from __future__ import annotations

import hashlib

# Sentinel hash used as the ``previous_hash`` for the very first audit entry.
GENESIS_HASH: str = "0" * 64


def hash_file(file_bytes: bytes) -> str:
    """Return the SHA-256 hex digest of *file_bytes*."""
    return hashlib.sha256(file_bytes).hexdigest()


def hash_string(text: str) -> str:
    """Return the SHA-256 hex digest of *text* (UTF-8 encoded)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def hash_chain_entry(entry_payload: str, previous_hash: str) -> str:
    """Return the SHA-256 hex digest of ``entry_payload + previous_hash``.

    This is the building block for the append-only audit hash chain.
    Each new audit entry's hash is derived from its own payload
    concatenated with the hash of the preceding entry, guaranteeing
    tamper-evidence.
    """
    return hashlib.sha256(
        (entry_payload + previous_hash).encode("utf-8")
    ).hexdigest()
