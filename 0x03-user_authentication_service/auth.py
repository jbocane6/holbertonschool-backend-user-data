#!/usr/bin/env python3
"""
This module contains the methods and attributes needed
for the authentication
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes.
    Args:
        password: The password to be encrypted.
    Returns:
        bytes: Salted hash of the input password, hashed with bcrypt.hashpw.
    """
    return hashpw(password.encode(), gensalt())
