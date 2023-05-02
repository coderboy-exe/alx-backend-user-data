#!/usr/bin/env python3
""" Auth module """
from flask import request
from typing import List, TypeVar


class Auth():
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns requre auth status """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path.rstrip("/")
        for ex_path in excluded_paths:
            if ex_path.rstrip("/") == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns auth header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user """
        return None
