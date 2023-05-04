#!/usr/bin/env python3
""" Session Auth module """
from .auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """ Session Auth class which inherits from Auth class """
    pass
