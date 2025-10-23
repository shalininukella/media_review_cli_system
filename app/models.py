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
    favourites = relationship("Favourites", back_populates="user") #for may to many for observer


class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # movie, show, song, # This column distinguishes the subclass

    reviews = relationship("Reviews", back_populates="media")
    favourited_by = relationship("Favourites", back_populates="media") #for may to many for observer

    __mapper_args__ = {
        "polymorphic_on" : type, # Tells SQLAlchemy to use 'type' for subclass mapping
        "polymorphic_identity": "media" # Identity for the base class
    }

#single table inheritance for all the media types for factory pattern
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

#association table or the bridge betweent User and the Media table to form many-to-many relationship btw them
class Favourites(Base):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    media_id = Column(Integer, ForeignKey("media.id"))

    user = relationship("User", back_populates="favourites")
    media = relationship("Media", back_populates="favourited_by")



