from sqlalchemy import Column, Integer, String, Float, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime

# ----------------- Reviews -----------------
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


# ----------------- Users -----------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    reviews = relationship("Reviews", back_populates="user")
    favourites = relationship("Favourites", back_populates="user")


# ----------------- Media -----------------
class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)  # movie, show, song

    reviews = relationship("Reviews", back_populates="media")
    favourited_by = relationship("Favourites", back_populates="media")

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "media"
    }

class Movie(Media):
    __mapper_args__ = {"polymorphic_identity": "movie"}

class Show(Media):
    __mapper_args__ = {"polymorphic_identity": "show"}

class Song(Media):
    __mapper_args__ = {"polymorphic_identity": "song"}


# ----------------- Favourites (association) -----------------
class Favourites(Base):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    media_id = Column(Integer, ForeignKey("media.id"))

    user = relationship("User", back_populates="favourites")
    media = relationship("Media", back_populates="favourited_by")
