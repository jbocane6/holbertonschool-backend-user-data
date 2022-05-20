#!/usr/bin/env python3
"""
User passwords should NEVER be stored in plain text in a database.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    function that expects one string argument name password
    and returns a salted, hashed password, which is a byte string.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Function that expects 2 arguments and returns a boolean
    to validate that the provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
