from sqlalchemy import Column, Integer, String, Enum
from app.db.base import Base
from enum import Enum as PyEnum

class Role(str, PyEnum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"

class Status(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(Role))
    status = Column(Enum(Status), default=Status.ACTIVE)