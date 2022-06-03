#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB():
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Implement the add_user method, which should save the user
        to the database.
        Arguments:
            email: A non-nullable string.
            hashed_password: A non-nullable string.
        Returns:
            User object.
        """
        if email is None or hashed_password is None or type(email) != str\
           or type(hashed_password) != str:
            return None
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Implement the DB.find_user_by method.
        This method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered
        by the method's input arguments
        Arguments:
            email: A non-nullable string.
            hashed_password: A non-nullable string.
        Returns:
            The first row found in the users table.
        """
        if kwargs is None:
            raise InvalidRequestError
        key_cols = User.__table__.columns.keys()
        for k in kwargs.keys():
            if k not in key_cols:
                raise InvalidRequestError
        rqrd_usr = self._session.query(User).filter_by(**kwargs).first()
        if rqrd_usr is None:
            raise NoResultFound
        return rqrd_usr
