#!/usr/bin/env python3
"""
Manages API Authentication.
"""

from flask import request
from typing import List, Union


class Auth:
    """A class to handle and manage API authentication
    """

    def __init__(self):
        """A constructor for the Auth class
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """A method that checks authentication
        """
        if not path or not excluded_paths:
            return True
        path = path.rstrip("/") + "/"

        for exc_path in excluded_paths:
            if path.startswith(exc_path.rstrip("*")):
                return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> Union[str, None]:
        """A method that checks the authorization header
        """
        if not request:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """Return the current user.
        """
        return None
