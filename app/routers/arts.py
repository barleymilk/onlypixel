import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, HTTPException, Path, Request, Form
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from cruds import main_crud, signup_crud
from funcs import signup_func
import schemas, models
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/arts",
    tags=["arts"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")

db_dependency = Annotated[Session, Depends(main_crud.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

## 아트페이지
@router.get("/", status_code=status.HTTP_200_OK)
async def arts(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("arts.html", {"request": request})

## 아트 단일 페이지
@router.get("/{art_id}", status_code=status.HTTP_200_OK)
async def read_one_art(art_id: int = Path(gt=0)):
    return {"art-id": art_id}

# 아트 작성
@router.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_art(user: user_dependency):
    return {"message": "아트 게시 완료"}

# 아트 수정(본인, 로그인)
@router.put("/{art_id}")
async def update_art(user: user_dependency, art_id: int = Path(gt=0)):
    art_changed = False
    # 수정 완료시 art_changed = True
    if not art_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "아트 내용 수정"}

# 아트 삭제(본인, 로그인)
@router.put("/{art_id}")
async def delete_art(user: user_dependency, art_id: int = Path(gt=0)):
    art_changed = False
    # 수정 완료시 art_changed = True
    if not art_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "아트 삭제"}