from fastapi import FastAPI, HTTPException, Depends, status, Body
from typing import Annotated
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import date, datetime, timedelta
import random

from app.schemas import Game, News, Community, User, Token, TokenData, UserInDB, UserCreate, UserLogin, GameCreate, NewsCreate

from dotenv import load_dotenv

from app import crud, models, schemas, database
from app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

load_dotenv()  # .env 파일을 활성화


## DEBUG--
import logging
import sys

mylogger = logging.getLogger("mylogger")

formatter = logging.Formatter('[%(levelname)s] %(message)s')

handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)

mylogger.addHandler(handler)
mylogger.setLevel(logging.DEBUG)
## --DEBUG



## 이메일 함수--

import smtplib
from email.message import EmailMessage
import os

# 이메일 중복 체크 함수
def check_duplicate_email(email: str):
    for user in fake_users_db:
        if user["email"] == email:
            return True
    return False

# 환경 변수에서 앱 비밀번호 가져오기
app_password = os.environ.get("GMAIL_APP_PASSWORD")

# 이메일 인증코드 생성 함수
def generate_verification_code():
    return str(random.randint(100000, 999999))

# 사용자의 이메일과 해당 인증코드, 생성 시간을 저장하는 딕셔너리
email_verification_codes = {}

# 이메일 발송 함수
def send_verification_email(email, code):
    subject = "Email Verification Code"
    message = f"Your verification code is: {code}"
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = subject
    msg["From"] = "barleymilk640@gmail.com"  # 발송 이메일 주소
    msg["To"] = email

    # Gmail 사용 예시
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("barleymilk640@gmail.com", app_password)  # 발송 이메일 계정 정보
    server.send_message(msg)
    server.quit()

## --이메일 함수



## 로그인 함수--

SECRET_KEY = "514957db8c767b7a475789e53f747fd0d3b31a4ac33f85a0b6fdee86a902b2f9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

## --로그인 함수



app = FastAPI()

## 메인페이지
@app.get("/")
async def root(db: Session = Depends(crud.get_db)):
    games = crud.get_games(db, limit=6)
    news = crud.get_news(db, limit=6)

    return {"games": games, "news": news}

### (임시) 게임 데이터 집어넣는 기능
@app.post("/games")
async def create_game(game: GameCreate, db: Session = Depends(database.get_db)):
    return crud.create_game(db, game)
### (임시) 뉴스 데이터 집어넣는 기능
@app.post("/news")
async def create_news(news: NewsCreate, db: Session = Depends(database.get_db)):
    return crud.create_news(db, news)


## 회원가입
@app.post("/register")
async def register(user: UserCreate):
    if check_duplicate_email(user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    verification_code = generate_verification_code()
    send_verification_email(user.email, verification_code)

    new_user = User(
        id=len(fake_users_db) + 1,
        email=user.email,
        password=user.password,
        phone_number=user.phone_number,
        nickname=user.nickname,
        birth_date=user.birth_date,
        profile_image=user.profile_image,
        created_at=datetime.now(),
        access_token="your_generated_access_token",
        reports=0
    )
    fake_users_db.append(new_user)

    # 이메일 인증코드 저장 : 인증코드, 생성시간, 만료시간(5분 설정)
    email_verification_codes[user.email] = {
        "code": verification_code,
        "creation_time": datetime.now(),
        "expiration_time": datetime.now() + timedelta(minutes=5)
    }

    return {"message": "User registered successfully"}

## 회원가입 > 이메일 검증
@app.post("/verify")
async def verify_email(email: str, code: str):
    if email in email_verification_codes:
        current_time = datetime.now()
        if current_time <= email_verification_codes[email]["expiration_time"]:
            if code == email_verification_codes[email]["code"]:
                return {"message": "Email verified successfully"}
    
    raise HTTPException(status_code=400, detail="Email verification failed")

## 로그인
@app.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# @app.get("/users/me/", response_model=User)
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return current_user

# @app.get("/users/me/items/")
# async def read_own_items(
#     current_user: Annotated[User, Depends(get_current_active_user)]
# ):
#     return [{"item_id": "Foo", "owner": current_user.username}]


## 뉴스페이지
@app.get("/news")
async def news():
    news = [News(**news_data) for news_data in _sample_news]
    return news

## 게임페이지
@app.get("/games")
async def games():
    games = [Game(**game_data) for game_data in _sample_games]
    return games

@app.get("/games/{game_id}")
async def games(game_id: int):
    game = None
    for _game_data in _sample_games:
        if _game_data['id'] == game_id:
            game = Game(**_game_data)
    return game

@app.post("/posts")
def create_post(post: Community):
    mylogger.debug(post)
    return None

# uvicorn main:app --reload