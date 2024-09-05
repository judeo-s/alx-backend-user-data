#!/usr/bin/env python3
""" Module of authentication """
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for authentication system for API/site access"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if a path requires authentication"""
        if path and excluded_paths:
            path = f'{path}/' if path[-1] != '/' else path
            for ex_path in excluded_paths:
                ex_path = f'{ex_path}/' if ex_path[-1] != '/' else ex_path
                if ex_path[-2] == '*':
                    if path[:-1].startswith(ex_path[:-2]):
                        return False
                if path == ex_path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieves a request's authorization header for authentication"""
        if not request or not request.headers.get('Authorization'):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a user object for an authenticated user"""
        return None
