#!/usr/bin/env python3

"""Auth module."""
import uuid
from typing import Union

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB

from user import User


def _hash_password(password: str) -> bytes:
    """Hash plaintext passwords."""
    return bcrypt.hashpw(password=password.encode(), salt=bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth object."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password.
        """
        if not email:
            raise ValueError("email missing")
        if not password:
            raise ValueError("password missing")

        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            pass
        else:
            raise ValueError(f"User {email} already exists")

        hashed_password = _hash_password(password=password).decode()
        return self._db.add_user(email=email, hashed_password=hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user login credentials.
        """
        try:
            db_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=db_user.hashed_password.encode(),
        )

    @staticmethod
    def _generate_uuid() -> str:
        """Generate UUIDs."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> Union[str, None]:
        """Create session for a user after successful login.
        """
        try:
            db_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        self._db.update_user(
            user_id=db_user.id, session_id=self._generate_uuid()
        )

        return db_user.session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Get the user object related with a session ID.
        """
        if not session_id:
            return None

        try:
            db_user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return db_user

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user session
        """
        try:
            self._db.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"{user_id} is not a valid user ID.")

        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Return the token for user password reset."""
        if not email:
            raise ValueError("email missing")

        try:
            db_user = self._db.find_user_by(email=email)
        except NoResultFound as err:
            raise ValueError(f"User with email {email} not found") from err

        reset_token = self._generate_uuid()
        self._db.update_user(user_id=db_user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Reset user password."""
        try:
            db_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Reset token is invalid or expired")

        hashed_password = _hash_password(password).decode()
        self._db.update_user(
            user_id=db_user.id,
            hashed_password=hashed_password,
            reset_token=None,  # expire the token
        )
