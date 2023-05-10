#!/usr/bin/env python3
""" Auth class module """
import bcrypt
import uuid

from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """ Hash password using bcrypt module """
    salt = bcrypt.gensalt()
    password_bytes = password.encode('utf-8')
    return bcrypt.hashpw(password_bytes, salt)


def _generate_uuid() -> str:
    """ Returns a stringified uuid """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
            Checks password to see if ti matches password hash for
            a given email.
        """
        try:
            user = self._db.find_user_by(email=email)
            encoded = password.encode('utf-8')
            return bcrypt.checkpw(encoded, user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """ Takes an email argument and returns the session ID """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Returns the user for a corresponding session_id """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ Destroys a user session. Returns Nothing """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            pass
