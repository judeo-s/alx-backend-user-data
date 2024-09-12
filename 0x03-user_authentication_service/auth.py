#!/usr/bin/env python3
"""
A module to handle things related to authentication
"""
import bcrypt


SALT = bcrypt.gensalt()

def _hash_password(password: str) -> bytes:
    """ A method that hashes a password using bcrypt hashing algorithm
    """
    return bcrypt.hashpw(password.encode("utf-8"), SALT)
