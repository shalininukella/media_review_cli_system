from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db import Base
import datetime


class Reviews(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    media_id = Column(Integer, ForeignKey("media.id"))
    rating = Column(Float)
    comment = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.datetime.now(datetime.timezone.utc))

    user = relationship("User", back_populates="reviews")
    media = relationship("Media", back_populates="reviews")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    reviews = relationship("Reviews", back_populates="user")


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # movie, show, song, # This column distinguishes the subclass

    reviews = relationship("Reviews", back_populates="media")

    __mapper_args__ = {
        "polymorphic_on" : type, # Tells SQLAlchemy to use 'type' for subclass mapping
        "polymorphic_identity": "media" # Identity for the base class
    }

#single table inheritance for all the media types
class Movie(Media):
    __mapper_args__ = {
        "polymorphic_identity": "movie" # Identity for Movie subclass
    }

class Show(Media):
    __mapper_args__ = {
        "polymorphic_identity" : "show"
    }

class Song(Media):
    __mapper_args__ = {
        "polymorphic_identity" : "song"
    }


