#!/usr/bin/env python3
"""
Module basic_auth
"""
from api.v1.auth.auth import Auth
from base64 import b64decode
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    Inherits from Auth
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Returns the Base64 part of the Authorization header
        for a Basic Authentication
        """
        if authorization_header and type(authorization_header) == str:
            return authorization_header.split(" ")[-1]
        if authorization_header.startswith('Basic '):
            return authorization_header[6:]
        return None
