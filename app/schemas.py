from pydantic import BaseModel, Field
from typing import List, Union, Optional
from datetime import date, datetime
from pydantic.networks import EmailStr


class EmailCodeCheck(BaseModel):
    email: EmailStr
    code: str
    creation_time: datetime
    expiration_time: datetime

class UserRegister(BaseModel):
    email: EmailStr
    hashed_password: str
    phone_number: str
    nickname: str = Field(min_length=1, max_length=10)
    birth_date: date
    profile_image: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "example@gmail.com",
                "hashed_password": "hashedpassword",
                "phone_number": "+821059545452",
                "nickname": "바다소금",
                "birth_date": "1999-03-24",
                "profile_image": "myprofile.png"
            }
        }

# class User(UserBase):
    # id: Optional[int] = Field(title="id is not needed")
#     email: str
#     hashed_password: str
#     phone_number: str
#     nickname: str
#     birth_date: date
#     profile_image: str
#     created_at: datetime
#     access_token: str
#     disabled: bool = False
#     reports: int = 0

class UserEmailCheck(BaseModel):
    email: EmailStr

class UserInDB(UserRegister):
    hashed_password: str


class Game(BaseModel):
    id: int
    title: str
    description: Union[str, None] = None
    price: int
    release_date: date
    early_access_release_date: date
    developer: str
    publisher: str
    genre: List[str]
    tags: List[str]
    languages: List[str]
    game_rating: Union[List[str], None] = None
    game_censorship: Union[List[str], None] = None
    platform: List[str]
    minimum_system_requirements: List[dict]
    recommended_system_requirements: List[dict]
    views: int = 0
    likes: int = 0
    purchase_link: str
    image_path: List[str]
    video_path: Optional[List[str]] = None
    
class GamesList(BaseModel):
    total: int = 0
    games_list: List[str]

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
    content_with_tag: str
    author: str
    written_date: datetime
    last_modified_date: datetime
    views: int = 0
    likes: int = 0
    image_path: Optional[List[str]] = None
    video_path: Optional[List[str]] = None

class NewsList(BaseModel):
    total: int = 0
    news_list: List[str]

class Post(BaseModel):
    id: int
    post_menu: str
    title: str = Field(min_length=1)
    content: str
    user_id: int
    written_date: datetime
    last_modified_date: datetime
    views: int = 0
    likes: int = 0
    image_path: Optional[List[str]] = None
    video_path: Optional[List[str]] = None
    reports: int = 0

class PostRequest(BaseModel):
    post_menu: str
    title: str = Field(min_length=1)
    content: str
    last_modified_date: datetime
    image_path: Optional[List[str]] = None
    video_path: Optional[List[str]] = None