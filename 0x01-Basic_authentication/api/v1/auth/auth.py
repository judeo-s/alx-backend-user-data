#!/usr/bin/env python3
"""
Manages API Authentication.
"""

from flask import request
from typing import List


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
        return False

    def authorization_header(self, request=None) -> str:
        """A method that checks the authorization header
        """
        return None
