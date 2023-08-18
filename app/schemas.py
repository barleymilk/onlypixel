from typing import List, Union, Optional
from datetime import date, datetime
from pydantic import BaseModel

class Game(BaseModel):
    id: int
    name: str
    description: Union[str, None] = None
    price: int
    release_date: date
    developer: str
    publisher: str
    genre: List[str]
    tags: List[str]
    game_rating: Union[List[str], None] = None
    game_censorship: Union[List[str], None] = None
    platform: List[str]
    game_requirements: List[dict]
    views: int = 0
    likes: int = 0
    purchase_link: str
    image_path: List[str]
    video_path: Optional[List[str]] = None


class GameCreate(BaseModel):
    name: str
    description: Union[str, None] = None
    price: int
    release_date: date
    developer: str
    publisher: str
    genre: List[str]
    tags: List[str]
    game_rating: Union[List[str], None] = None
    game_censorship: Union[List[str], None] = None
    platform: List[str]
    game_requirements: List[dict]
    views: int = 0
    likes: int = 0
    purchase_link: str
    image_path: List[str]
    video_path: Optional[List[str]] = None


class News(BaseModel):
    id: int
    title: str
    content: str
    author: str
    written_date: datetime
    last_modified_date: datetime
    views: int = 0
    likes: int = 0
    image_path: Optional[List[str]] = None
    video_path: Optional[List[str]] = None

class NewsCreate(BaseModel):
    title: str
    content: str
    author: str
    written_date: datetime
    last_modified_date: datetime
    views: int = 0
    likes: int = 0
    image_path: Optional[List[str]] = None
    video_path: Optional[List[str]] = None

class Community(BaseModel):
    id: int
    post_menu: str
    title: str
    content: str
    user_id: int
    written_date: datetime
    last_modified_date: datetime
    views: int = 0
    likes: int = 0
    image_path: Optional[List[str]] = None
    video_path: Optional[List[str]] = None
    reports: int = 0

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    email: str
    hashed_password: str
    phone_number: str
    nickname: str
    birth_date: date
    profile_image: str
    created_at: datetime
    access_token: str
    disabled: bool = False
    reports: int = 0


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class UserCreate(BaseModel):
    email: str
    hashed_password: str
    phone_number: str
    nickname: str
    birth_date: date
    profile_image: str


class UserLogin(BaseModel):
    email: str
    hashed_password: str


class Comment(BaseModel):
    id: int
    commu_id: int
    user_id: int
    written_date: datetime
    last_modified_date: datetime
    content: str
    likes: int = 0
    reports: int = 0



class LoginHistory(BaseModel):
    id: int
    user_id: int
    login_time: datetime
    status: str



class NewsGame(BaseModel):
    id: int
    news_id: int
    game_id: int


class CommunityGame(BaseModel):
    id: int
    commu_id: int
    game_id: int


class UserLikedGame(BaseModel):
    id: int
    user_id: int
    game_id: int
    time: datetime


class UserPostedCommunity(BaseModel):
    id: int
    user_id: int
    commu_id: int


class UserPostedComment(BaseModel):
    id: int
    user_id: int
    comment_id: int


class UserLikedNews(BaseModel):
    id: int
    user_id: int
    news_id: int
    time: datetime


class UserLikedCommunity(BaseModel):
    id: int
    user_id: int
    commu_id: int
    time: datetime