#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    @staticmethod
    def valid_attributes(**kwargs) -> bool:
        """Validate keyword arguments against User class attributes.
        """
        user_dict_keys = set(User.__dict__.keys())
        kw_dict_keys = set(kwargs.keys())

        if not kw_dict_keys.issubset(user_dict_keys):
            return False
        return True

    def add_user(self, email: str, hashed_password: str) -> User:
        """An instance method to add a user to the database
        """
        db_user = User(email=email, hashed_password=hashed_password)
        sel._session.add(db_user)
        self._session.commit()

        return db_user

    @staticmethod
    def find_user_by(self, **kwargs) -> User:
        """Search and return user by a given field.
        """
        if not kwargs:
            raise InvalidRequestError("No search parameters provided.")

        if not self.valid_attributes(**kwargs):
            raise InvalidRequestError("Invalid search parameters provided.")

        db_user = self._session.query(User).filter_by(**kwargs).first()
        if not db_user:
            raise NoResultFound("No user found with the given parameters.")
        return db_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update an instance of a user.
        """
        if not self._valid_attributes(**kwargs):
            raise ValueError("Unrecognized arguments for User.")

        db_user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            setattr(db_user, key, value)

        self._session.add(db_user)
        self._session.commit()
