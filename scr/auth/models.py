from datetime import datetime

from sqlalchemy import Integer, String, Column, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


class ReferalCode(Base):
    __tablename__ = 'referal_code'
    id = Column(Integer, primary_key=True)
    creator = Column(Integer, ForeignKey(User.id))
    referal_code = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    date_of_createion = Column(TIMESTAMP, default=datetime.utcnow)
    lifetime = Column(TIMESTAMP, nullable=False)


class Member(Base):
    __tablename__ = 'member'
    id = Column(Integer, primary_key=True)
    referal_code = Column(Integer, ForeignKey('referal_code.id'))
    referal = Column(Integer, ForeignKey(User.id))