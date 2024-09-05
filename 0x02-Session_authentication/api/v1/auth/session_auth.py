#!/usr/bin/env python3
"""Module for session authentication"""
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Session authentication system for API/site access"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a user/logs user-in if the given ID exists"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = uuid4().__str__()
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user ID that owns the session with given ID if exits"""
        if not session_id or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns a user object for an authenticated user"""
        if not request:
            return None
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User().get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Deletes the current session/logs-out"""
        if not request:
            return False
        # Get and delete session for current request if it exists
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
