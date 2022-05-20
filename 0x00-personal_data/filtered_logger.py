#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the log message obfuscated:
"""
from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Returns the log message obfuscated"""
    for i in fields:
        response = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator, message)
    return response
