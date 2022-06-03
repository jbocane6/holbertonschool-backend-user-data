#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


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
            kwargs: key word based argument
        Returns:
            The first row found in the users table.
        """
        if kwargs is None:
            raise InvalidRequestError
        key_cols = User.__table__.columns.keys()
        for k in kwargs.keys():
            if k not in key_cols:
                raise InvalidRequestError
        rqrd_user = self._session.query(User).filter_by(**kwargs).first()
        if rqrd_user is None:
            raise NoResultFound
        return rqrd_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Implement the DB.update_user method
        that takes as argument a required user_id integer
        and arbitrary keyword arguments, and returns None.
        Arguments:
            user_id - the given user id
        """
        if kwargs is None:
            return None
        rqrd_user = self.find_user_by(id=user_id)
        key_cols = User.__table__.columns.keys()
        for k in kwargs:
            if k not in key_cols:
                raise ValueError

        for k, v in kwargs.items():
            setattr(rqrd_user, k, v)
        self._session.commit()
