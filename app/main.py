from typing import Annotated
from fastapi import FastAPI, Request, HTTPException, Depends, Path, Query
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from starlette import status
import datetime
import json

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from logging_config import mylogger
from routers import auth, news, games, arts, mini_games, posts
from cruds import main_crud, signup_crud
from funcs import signup_func
import schemas, models
from routers.auth import get_current_user

from dotenv import load_dotenv
load_dotenv()  # .env 파일을 활성화

app = FastAPI()
app.include_router(auth.router)
app.include_router(news.router)
app.include_router(games.router)
app.include_router(arts.router)
app.include_router(mini_games.router)
app.include_router(posts.router)

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
templates = Jinja2Templates(directory="../templates")

db_dependency = Annotated[Session, Depends(main_crud.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

## 메인페이지
@app.get("/", status_code=status.HTTP_200_OK)
async def root(request: Request, response_class=HTMLResponse, db: Session = Depends(main_crud.get_db)):
    games = main_crud.get_games(db, limit=6)
    news = main_crud.get_news(db, limit=6)
    return templates.TemplateResponse("home.html", {"request": request, "games": games, "news": news})

## 회원가입
@app.get("/signup", status_code=status.HTTP_200_OK)
async def signup(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", status_code=status.HTTP_201_CREATED)
async def post_email(email_check: schemas.UserEmailCheck, db: Session = Depends(main_crud.get_db)):
    # 이메일 중복 확인
    if signup_crud.check_duplicate_email(db, email_check.email):
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    # 이메일 중복 없는 경우 > 인증코드 보내기 & 이메일 인증코드 작성페이지로 넘어가기
    else:
        verification_code = signup_func.generate_verification_code()
        signup_func.send_verification_email(user.email, verification_code)
        return {"message": "해당 이메일로 인증 코드를 보냈습니다."}

# /verify : 이메일 인증 코드 작성하는 곳
@app.get("/verify", status_code=status.HTTP_200_OK)
async def verify(request: Request, response_class=HTMLResponse):
    return {"message": "이메일 인증 코드를 작성해주세요."}

@app.post("/verify", status_code=status.HTTP_201_CREATED)
async def post_code():
    return {"message": "인증 코드를 확인했습니다!"}

# /register : 유저 정보 작성하는 곳 > 비밀번호 규칙 확인, 닉네임 유일성 확인 > 비밀번호 해싱, 정보 User DB 저장 > 로그인 페이지로 이동
@app.get("/register", status_code=status.HTTP_200_OK)
async def register(request: Request, response_class=HTMLResponse):
    return {"message": "유저 정보를 작성해주세요."}

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def post_user_info(user_info: schemas.UserRegister):
    return {"message": "회원가입이 완료되었습니다:D\n로그인 해주세요!"}

## 로그인
@app.get("/login")
async def login(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("login.html", {"request": request})

# 로그인 성공시 메인페이지로 이동
@app.post("/login")
async def post_login_info():
    # 유저 정보 조회
    # 이메일 없거나 비밀번호 틀리면 > 404 not found 에러가 아니라 authorization 에러? 뭔가일듯
    # 둘 다 맞으면 이동
    return {"message": "로그인 성공! 메인페이지 이동"}

## 로그아웃(상태: 로그인) > 메인페이지로 이동

## 마이페이지(상태: 로그인)
@app.get("/me")
async def me(user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Autnehtication Failed')
    # todo_model = Todos(**todo_request.dict(), owner_id=user.get('id'))
    return {"message": "마이페이지입니다."}

# 개인정보 수정(상태: 로그인)
@app.patch("/me", status_code=status.HTTP_204_NO_CONTENT)
async def update_password():
    password_changed = False
    # 비밀번호 수정 완료시 password_changed = True
    if not password_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "비밀번호 수정"}

# 회원 탈퇴(상태: 로그인)
@app.post("/me")
async def delete_account(user: user_dependency):
    return {"message": "회원 탈퇴 요청이 완료되었습니다."}

@app.get("/liked-games", status_code=status.HTTP_200_OK)
async def liked_games(user: user_dependency):
    return {"message": "찜한 게임입니다."}

@app.get("/liked-posts", status_code=status.HTTP_200_OK)
async def liked_posts(user: user_dependency):
    return {"message": "좋아요한 게시글입니다."}

@app.get("/liked-news", status_code=status.HTTP_200_OK)
async def liked_news(user: user_dependency):
    return {"message": "좋아요한 뉴스입니다."}

@app.get("/my-posts", status_code=status.HTTP_200_OK)
async def my_posts(user: user_dependency):
    return {"message": "작성한 게시글입니다."}

@app.get("/my-comments", status_code=status.HTTP_200_OK)
async def my_comments(user: user_dependency):
    return {"message": "작성한 댓글입니다."}