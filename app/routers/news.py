import sys, os
from pydantic import BaseModel
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, Path, Request, Form
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from cruds import main_crud, signup_crud, news_crud
from funcs import signup_func
import schemas, models
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/news",
    tags=["news"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")

db_dependency = Annotated[Session, Depends(main_crud.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

## 뉴스페이지
@router.get("/", response_model=schemas.NewsList, status_code=status.HTTP_200_OK)
async def news(db: db_dependency, request: Request, response_class=HTMLResponse,
               page: int = 0):
    total, _news_list = news_crud.get_news_list(db, skip=page*10, limit=10)
    return templates.TemplateResponse("news.html", {"request": request, "total": total, "page": page, "news_list": _news_list})

@router.post("/")
async def news_search(search: str):
    return {"message": "뉴스 검색어 입력"}

## 뉴스 단일 페이지
@router.get("/{news_id}", status_code=status.HTTP_200_OK)
async def read_one_news(db:db_dependency, request: Request, response_class=HTMLResponse, news_id: int = Path(gt=0)):
    news_item = db.query(models.News).filter(models.News.id == news_id).first()
    return templates.TemplateResponse("news_detail.html", {"request": request, "news_item": news_item})