#!/usr/bin/env python3
""" Module of authentication """
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii


class BasicAuth(Auth):
    """Basic authentication system for API/site access"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Retrieves authorization string from request header"""
        if not authorization_header\
                or not isinstance(authorization_header, str)\
                or not authorization_header.split()[0] == 'Basic':
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Converts a base64 string to a regular/UTF-8 string"""
        if not base64_authorization_header\
                or not isinstance(base64_authorization_header, str):
            return None
        auth_str = base64_authorization_header
        try:
            return base64.b64decode(auth_str).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Creates creds tuple (user, pwd) from decoded authorization string"""
        if not decoded_base64_authorization_header\
                or not isinstance(decoded_base64_authorization_header, str)\
                or ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(sep=':',
                                                               maxsplit=1))

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Creates a user object for the given credentials"""
        if not user_email or not isinstance(user_email, str)\
                or not user_pwd or not isinstance(user_pwd, str):
            return None
        user = User().search({'email': user_email})
        if user:
            return user[0] if user[0].is_valid_password(user_pwd) else None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a user object for an authenticated user"""
        if not request:
            return None
        auth = self.authorization_header(request)
        auth = self.extract_base64_authorization_header(auth) if auth else None
        auth = self.decode_base64_authorization_header(auth) if auth else None
        auth = self.extract_user_credentials(auth) if auth else None
        user = self.user_object_from_credentials(*auth) if auth else None
        return user
