#!/usr/bin/env python3
""" Module definition """
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """ Returns obfuscated log message """
    for field in fields:
        message = re.sub(fr'({field})=([^{separator}]*)', fr'\1={redaction}',
                         message)
    return message
