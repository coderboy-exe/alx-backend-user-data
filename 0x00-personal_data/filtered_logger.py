#!/usr/bin/env python3
""" Module definition """
import re
import logging
import os
import mysql.connector
from typing import List


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns obfuscated log message """
    for field in fields:
        message = re.sub(fr'({field})=([^{separator}]*)', fr'\1={redaction}',
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ class initializaton method """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ filter and format values in incomin log records """
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """ returns logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ initialize db connection """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST") or "localhost",
        user=os.getenv("PERSONAL_DATA_DB_USERNAME") or "root",
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD") or "",
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )


def main():
    """ entry point for db connection """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    fields = ('name', 'email', 'phone', 'ssn', 'password', 'ip',
              'last_login', 'user_agent')
    for row in rows:
        message = "".join((f"{k}={v}; " for k, v in zip(fields, row)))
        logger.info(message)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
