import enum

from sqlalchemy import Column, Integer, String, Enum
from .database import Base


class UserRole(enum.Enum):
    SPORTSMAN = 'SPORTSMAN'
    ORG = 'ORG'
    BUSINESS_PARTNER = 'BUSINESS_PARTNER'


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
