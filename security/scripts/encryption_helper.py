"""Utility functions for AES-256 encryption and decryption.

This module expects the environment variable `GF_ENC_KEY` to be set via
Replit Secrets or another secure store. The key should be a strong
passphrase. It is encoded with URL-safe base64 to generate the symmetric
key used by ``cryptography``'s :class:`Fernet` helper.
"""

from __future__ import annotations

import base64
import os
from cryptography.fernet import Fernet


def _load_fernet() -> Fernet:
    """Return a :class:`Fernet` instance initialized from ``GF_ENC_KEY``."""
    secret = os.getenv("GF_ENC_KEY")
    if not secret:
        raise RuntimeError("GF_ENC_KEY environment variable not set")
    key = base64.urlsafe_b64encode(secret.encode())
    return Fernet(key)


_f = _load_fernet()


def seal(plaintext: bytes) -> bytes:
    """Encrypt ``plaintext`` using AES-256 (Fernet)."""
    return _f.encrypt(plaintext)


def open(ciphertext: bytes) -> bytes:
    """Decrypt ``ciphertext`` that was produced by :func:`seal`."""
    return _f.decrypt(ciphertext)
