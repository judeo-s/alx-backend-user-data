#!/usr/bin/env python3
"""
A module to handle things related to authentication
"""
import bcrypt
from db import DB, NoResultFound, InvalidRequestError
from user import User
from uuid import uuid4


SALT = bcrypt.gensalt()


def _hash_password(password: str) -> bytes:
    """ A method that hashes a password using bcrypt hashing algorithm
    """
    return bcrypt.hashpw(password.encode("utf-8"), SALT)


def _generate_uuid() -> str:
    """A method that returns a uuid4 string
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """A constructor for the Auth class
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """A function to register users into the database.
        """
        try:
            found_user = self._db.find_user_by(email=email)
        except NoResultFound:
            found_user = None

        if found_user:
            raise ValueError(f"User {email} already exists")

        new_user = self._db.add_user(
                email, _hash_password(password).decode("utf-8"))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """An instance method to check if the password matches the hashed
        password in the datbase.
        """
        found_user = None
        try:
            found_user = self._db.find_user_by(email=email)
        except InvalidRequestError:
            return False
        except NoResultFound:
            return False

        return bcrypt.checkpw(
                password.encode("utf-8"),
                found_user.hashed_password.encode("utf-8"))

    def create_session(self, email: str) -> str:
        """A method used to create a sesison for a registered user.
        """
        found_user = None
        try:
            found_user = self._db.find_user_by(email=email)
        except InvalidRequestError:
            return None
        except NoResultFound:
            return None

        return _generate_uuid()
