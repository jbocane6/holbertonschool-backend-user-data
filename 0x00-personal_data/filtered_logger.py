#!/usr/bin/env python3
"""
Write a function called filter_datum that returns the log message obfuscated:
"""
from typing import List
from os import getenv
import mysql.connector
import re
import logging


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        RedactingFormatter constructor.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filter values in incoming log records using filter_datum.
        Values for fields in fields should be filtered.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    for i in fields:
        message = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator, message)
    return message


def get_logger() -> logging.Logger:
    """
    Function that returns a logging object
    """
    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_h = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    log.setFormatter(formatter)
    log.addHandler(stream_h)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to a mysql database
    """
    db_connection = mysql.connector.connection.MySQLConnection(
        user=getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=getenv('PERSONAL_DATA_DB_NAME'))

    return db_connection


def main():
    """
    Will obtain a database connection using get_db
    and retrieve all rows in the users table
    and display each row under a filtered format
    """
    my_db = get_db()
    db_cursor = my_db.cursor()
    db_cursor.execute("SELECT * FROM users;")
    response = db_cursor.fetchall()

    fields = [i[0] for i in db_cursor.description]

    log = get_logger()

    for row in response:
        _row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(_row.strip())

    db_cursor.close()
    my_db.close()
