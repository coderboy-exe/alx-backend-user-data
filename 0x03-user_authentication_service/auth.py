#!/usr/bin/env python3
""" Auth class module """
import bcrypt

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hash password using bcrypt module """
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ Initialization attributes """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Register user.
            Args:
                email: string,
                password: string
            Returns: newly created user
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

