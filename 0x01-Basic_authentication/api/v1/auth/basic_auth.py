#!/usr/bin/env python3

"""This module implements the Basic Authentication mechanism."""
import base64
import binascii
from typing import Tuple, TypeVar, Union

from api.v1.auth.auth import Auth
from models.user import User as DBUser

User = TypeVar("User")


class BasicAuth(Auth):
    """BasicAuth class to manage the API authentication."""

    @staticmethod
    def extract_base64_authorization_header(authorization_header: str):
        """Return the value of the Authorization header."""
        if not authorization_header or not isinstance(
            authorization_header, str
        ):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]

    @staticmethod
    def decode_base64_authorization_header(
        base64_authorization_header: str,
    ):
        """Decode a base64 string."""
        if not base64_authorization_header or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            return base64.b64decode(
                base64_authorization_header.encode("utf-8")
            ).decode("utf-8")
        except binascii.Error:
            return None

    @staticmethod
    def extract_user_credentials(
        user_credentials: str,
    ) -> Union[Tuple[None, None], Tuple[str, str]]:
        """Extract the user credentials."""
        if not user_credentials or not isinstance(user_credentials, str):
            return None, None

        if ":" not in user_credentials:
            return None, None

        username, password = user_credentials.split(":", 1)

        return username, password

    @staticmethod
    def user_object_from_credentials(
        user_email: str, user_pwd: str
    ) -> Union[User, None]:
        """Return the User instance based on email and password."""
        if not user_email or not isinstance(user_email, str):
            return None

        if not user_pwd or not isinstance(user_pwd, str):
            return None

        try:
            db_user = DBUser.search({"email": user_email})
        except KeyError:
            return None

        if db_user and db_user[0].is_valid_password(user_pwd):
            return db_user[0]

        return None

    def current_user(self, request=None) -> User:
        """Return the current authenticated user."""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )
        if not base64_auth_header:
            return None

        decoded_base64_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        if not decoded_base64_auth_header:
            return None

        user_credentials = self.extract_user_credentials(
            decoded_base64_auth_header
        )
        if not user_credentials:
            return None

        user_email, user_pwd = user_credentials
        return self.user_object_from_credentials(user_email, user_pwd)
