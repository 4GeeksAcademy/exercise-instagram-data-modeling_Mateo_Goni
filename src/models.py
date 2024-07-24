import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    posts = relationship('Post', back_populates='author')
    followers = relationship('Follower', foreign_keys='Follower.user_to_id', back_populates='user_to')
    comments = relationship('Comment', back_populates='author')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    media = relationship('Media', back_populates='post')

class Follower(Base):
    __tablename__ = 'follower'
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_to_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='followers')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followers')

class Comment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    author = relationship('User', back_populates='comments')
    post = relationship('Post', back_populates='comments')

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False) 
    url = Column(String(250), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'))
    post = relationship('Post', back_populates='media')

def to_dict(self):
    return {}

# Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
