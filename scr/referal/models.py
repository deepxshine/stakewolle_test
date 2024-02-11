from sqlalchemy import Column, Integer, ForeignKey, String, Boolean, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

from auth.models import User

Base = declarative_base()


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
