#!/usr/bin/env python3
""" Module definition """
import bcrypt


def hash_password(password: str) -> bytes:
    """ returns a salted, hashed passwod, whuch is a byte string """
    b = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(b, salt)
    return hashed_pw


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ validate that the provided password matches the hashed password """
    b = password.encode('utf-8')
    check = bcrypt.checkpw(b, hashed_password)
    return check
