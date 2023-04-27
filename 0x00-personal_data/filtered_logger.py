#!/usr/bin/env python3
""" Module definition """
import re


def filter_datum(fields, redaction, message, separator):
    pattern = '|'.join(fields)
    r = re.sub(fr'({pattern})=([^{separator}]*)', fr'\1={redaction}', message)
    return r
