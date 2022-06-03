#!/usr/bin/env python3
"""
This module contains the methods and attributes needed
for the authentication
"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user in database.
        Args:
            email: A non-nullable string.
            password: A non-nullable string.
        Raises:
            ValueError: User already exists.
        Returns:
            User: User object.
        """
        try:
            users_found = self._db.find_user_by(email=email)
            if users_found:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Login method.
        Args:
            email: A non-nullable string.
            password: A non-nullable string.
        Returns:
            bool: True if login, False otherwise.
        """
        if not email or not password:
            return False
        try:
            users_found = self._db.find_user_by(email=email)
            hashed_password = users_found.hashed_password
            return checkpw(password.encode(),
                           hashed_password.encode('utf-8'))
        except (NoResultFound, InvalidRequestError):
            return False


def _hash_password(password: str) -> bytes:
    """
    Takes in a password string arguments and returns bytes.
    Args:
        password: The password to be encrypted.
    Returns:
        bytes: Salted hash of the input password, hashed with bcrypt.hashpw.
    """
    return hashpw(password.encode(), gensalt())
