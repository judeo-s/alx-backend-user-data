#!/usr/bin/env python3
"""Module for session authentication with session expiration"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session expiration for session authentication system"""
    def __init__(self):
        """Initialises an instance of this class"""
        tmp = getenv('SESSION_DURATION')
        self.session_duration = int(tmp) if tmp and tmp.isnumeric() else 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a user/logs user-in if the given ID exists"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dictionary = {'user_id': user_id,
                              'created_at': datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user ID that owns the session with given ID if exits"""
        if not session_id or not isinstance(session_id, str):
            return None
        session = self.user_id_by_session_id.get(session_id)
        if not session:
            return None
        user_id = session.get('user_id')
        if self.session_duration <= 0:
            return user_id
        created_at = session.get('created_at')
        if not created_at:
            return None
        # Check if session has expired
        created_at += timedelta(seconds=self.session_duration)
        if datetime.now() <= created_at:
            return user_id
