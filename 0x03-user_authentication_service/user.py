#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_password = Column(String(250))
    session_id = Column(String(250))
    reset_token = Column(String(250))

    def __repr__(self):
        return "<User(email='%s', hashed_password='%s', session_id='%s',\
                      reset_token='%s')>" % (self.email, self.hashed_password,
                                             self.session_id, self.reset_token)
