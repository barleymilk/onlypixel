from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATE, TIMESTAMP, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from sqlalchemy.dialects.mysql import LONGTEXT

from .database import Base

class Game(Base):
    __tablename__ = 'game'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(LONGTEXT, nullable=True)
    price = Column(INTEGER(unsigned=True), nullable=False, default=0)
    release_date = Column(DATE, nullable=True)
    developer = Column(String(50), nullable=False)
    publisher = Column(String(50), nullable=False)
    genre = Column(JSON, nullable=False)
    tags = Column(JSON, nullable=False)
    game_rating = Column(JSON, nullable=True)
    game_censorship = Column(JSON, nullable=True)
    platform = Column(JSON, nullable=False)
    game_requirements = Column(JSON, nullable=False)
    views = Column(INTEGER(unsigned=True), nullable=False, default=0)
    likes = Column(INTEGER(unsigned=True), nullable=False, default=0)
    purchase_link = Column(String(255), nullable=False)
    image_path = Column(JSON, nullable=False)
    video_path = Column(JSON, nullable=True)


class News(Base):
    __tablename__ = 'news'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(50), nullable=False)
    written_date = Column(TIMESTAMP, nullable=False, default=func.now())
    last_modified_date = Column(TIMESTAMP, nullable=True)
    views = Column(INTEGER(unsigned=True), nullable=False, default=0)
    likes = Column(INTEGER(unsigned=True), nullable=False, default=0)
    image_path = Column(JSON, nullable=True)
    video_path = Column(JSON, nullable=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    phone_number = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    birth_date = Column(DATE, nullable=False)
    profile_image = Column(String(255), nullable=False)
    reports = Column(INTEGER(unsigned=True), nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=False)
    access_token = Column(String(50), nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)

    login_history = relationship("LoginHistory", back_populates="user")
    communities = relationship("Community", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class LoginHistory(Base):
    __tablename__ = 'login_history'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=False)
    login_time = Column(TIMESTAMP, nullable=False)
    status = Column(String(50), nullable=False)

    user = relationship("User", back_populates="login_history")


class Community(Base):
    __tablename__ = 'community'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    post_menu = Column(String(50), nullable=False)
    title = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=True)
    written_date = Column(TIMESTAMP, nullable=False, default=func.now())
    last_modified_date = Column(TIMESTAMP, nullable=True)
    views = Column(INTEGER(unsigned=True), nullable=False, default=0)
    likes = Column(INTEGER(unsigned=True), nullable=False, default=0)
    image_path = Column(String(50), nullable=True)
    video_path = Column(String(50), nullable=True)
    reports = Column(INTEGER(unsigned=True), nullable=False, default=0)
    
    user = relationship("User", back_populates="communities")
    comments = relationship("Comment", back_populates="community")


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    commu_id = Column(INTEGER(unsigned=True), ForeignKey('community.id'), nullable=False)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=False)
    written_date = Column(TIMESTAMP, nullable=False, default=func.now())
    last_modified_date = Column(TIMESTAMP, nullable=True)
    content = Column(String(50), nullable=False)
    likes = Column(INTEGER(unsigned=True), nullable=False, default=0)
    reports = Column(INTEGER(unsigned=True), nullable=False, default=0)

    user = relationship("User", back_populates="comments")
    community = relationship("Community", back_populates="comments")


class NewsGame(Base):
    __tablename__ = 'news_game'

    id = Column(INTEGER(unsigned=True), primary_key=True)
    news_id = Column(INTEGER(unsigned=True), ForeignKey('news.id'), nullable=True)
    game_id = Column(INTEGER(unsigned=True), ForeignKey('game.id'), nullable=True)


class CommunityGame(Base):
    __tablename__ = 'community_game'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    commu_id = Column(INTEGER(unsigned=True), ForeignKey('community.id'), nullable=True)
    game_id = Column(INTEGER(unsigned=True), ForeignKey('game.id'), nullable=True)


class UserLikedGame(Base):
    __tablename__ = 'user_liked_game'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=True)
    game_id = Column(INTEGER(unsigned=True), ForeignKey('game.id'), nullable=True)
    time = Column(TIMESTAMP, nullable=True)


class UserLikedNews(Base):
    __tablename__ = 'user_liked_news'

    id = Column(INTEGER(unsigned=True), primary_key=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=True)
    news_id = Column(INTEGER(unsigned=True), ForeignKey('news.id'), nullable=True)
    time = Column(TIMESTAMP, nullable=True)


class UserLikedCommunity(Base):
    __tablename__ = 'user_liked_community'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=True)
    commu_id = Column(INTEGER(unsigned=True), ForeignKey('community.id'), nullable=True)
    time = Column(TIMESTAMP, nullable=True)


class UserPostedCommunity(Base):
    __tablename__ = 'user_posted_community'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=True)
    commu_id = Column(INTEGER(unsigned=True), ForeignKey('community.id'), nullable=True)


class UserPostedComment(Base):
    __tablename__ = 'user_posted_comment'

    id = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True)
    user_id = Column(INTEGER(unsigned=True), ForeignKey('user.id'), nullable=True)
    comment_id = Column(INTEGER(unsigned=True), ForeignKey('comment.id'), nullable=True)