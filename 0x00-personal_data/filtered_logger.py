#!/usr/bin/env python3
""" Module definition """
import re


def filter_datum(fields, redaction, message, separator):
    """ Returns obfuscated log message """
    for field in fields:
        pattern = fr'({field})=([^{separator}]*)'
        message = re.sub(pattern, fr'\1={redaction}', message)
    return message
