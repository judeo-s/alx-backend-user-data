#!/usr/bin/env python3
"""Module for DB management in session authentication system with expiration"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta

UserSession.load_from_file()


class SessionDBAuth(SessionExpAuth):
    """DB logic for session authentication system with expiration"""
    def create_session(self, user_id: str = None) -> str:
        """Creates a session for a user/logs user-in if the given ID exists"""
        session_id = super().create_session(user_id)
        if session_id:
            session = UserSession(user_id=user_id, session_id=session_id)
            session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user ID that owns the session with given ID if exits"""
        if session_id:
            session = UserSession().search({'session_id': session_id})
            if session:
                session = session[0]
                if self.session_duration <= 0:
                    return session.user_id
                # Check if session has expired
                lifespan = timedelta(seconds=self.session_duration)
                age = session.created_at + lifespan
                if datetime.utcnow() <= age:
                    return session.user_id

    def destroy_session(self, request=None) -> bool:
        """Deletes the current session/logs-out"""
        if not request:
            return False
        # Get and delete session for current request if it exists
        session_id = super().session_cookie(request)
        # if not session_id:
        if not session_id or not self.user_id_for_session_id(session_id):
            return False
        session = UserSession().search({'session_id': session_id})
        if session:
            session[0].remove()
            return True
        return False
