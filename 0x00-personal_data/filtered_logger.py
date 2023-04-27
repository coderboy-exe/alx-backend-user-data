#!/usr/bin/env python3
""" Module definition """
import re


def filter_datum(fields, redaction, message, separator):
    """
        Returns obfuscated log message:
        Arguments:
            fields: a list of strings representing all fields
            redaction:
            message:
            separator:
    """

    pattern = '|'.join(fields)
    r = re.sub(fr'({pattern})=([^{separator}]*)', fr'\1={redaction}', message)
    return r
