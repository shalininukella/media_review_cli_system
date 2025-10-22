from app.db import Base
from sqlalchemy import Column, Integer, String, Float, TIMESTAMP, ForeignKey
import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    reviews = relationship("Review", back_populates="user")

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    title = Column(String, )
