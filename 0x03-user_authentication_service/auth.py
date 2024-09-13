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
        found_user = self.search_user(email=email)

        if found_user:
            raise ValueError(f"User {email} already exists")

        new_user = self._db.add_user(
                email, _hash_password(password).decode("utf-8"))
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """An instance method to check if the password matches the hashed
        password in the datbase.
        """
        found_user = self.search_user(email=email)
        if not found_user:
            return False

        return bcrypt.checkpw(
                password.encode("utf-8"),
                found_user.hashed_password.encode("utf-8"))

    @staticmethod
    def _generate_uuid() -> str:
        """A method that returns a uuid4 string
        """
        return str(uuid4())

    def create_session(self, email: str) -> str:
        """A method used to create a sesison for a registered user.
        """
        user = self.search_user(email=email)
        session_id = None
        if user:
            session_id = Auth._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)

        return session_id

    def delete_session(self, session_id: str) -> bool:
        """ A method used to delete session_id
        """
        user = self.search_user(session_id=session_id)
        if user:
            self._db.update_user(user.id, session_id=None)
            return True
        else:
            return False

    def user_email_by_session_id(self, session_id: str) -> str:
        """A method used to return the email of a user using the session ID
        """
        user = self.search_user(session_id=session_id)
        if user:
            return user.email
        else:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """A method used to reset password token
        """
        user = self.search_user(email=email)
        if user:
            token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        else:
            raise ValueError("user does not exist")

    def search_user(self, **kwargs):
        """A method to find user from details
        """
        found_user = None
        try:
            print(kwargs)
            found_user = self._db.find_user_by(**kwargs)
        except InvalidRequestError:
            return None
        except NoResultFound:
            return None
        return found_user
