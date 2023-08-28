import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, Path, Request, Form
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

from cruds import main_crud, signup_crud, games_crud
from funcs import signup_func
import schemas, models
from .auth import get_current_user

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/games",
    tags=["games"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")

db_dependency = Annotated[Session, Depends(main_crud.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

## 게임페이지
@router.get("/", response_model=schemas.GamesList, status_code=status.HTTP_200_OK)
async def games(db: db_dependency, request: Request, response_class=HTMLResponse,
                page: int = 0):
    total, _games_list = games_crud.get_games_list(db, skip=page*10, limit=10)
    return templates.TemplateResponse("games.html", {"request": request, "total": total, "page": page, "games_list": _games_list})

# 게임페이지 with parameters
@router.get("/", status_code=status.HTTP_200_OK)
async def games():
    return {"message": "조건에 맞는 게임"}

## 게임 단일 페이지
@router.get("/{game_id}", status_code=status.HTTP_200_OK)
async def read_one_game(db:db_dependency, request: Request, response_class=HTMLResponse,
                        game_id: int = Path(gt=0)):
    game_item = db.query(models.Game).filter(models.Game.id == game_id).first()
    return templates.TemplateResponse("games_detail.html", {"request": request, "game_item": game_item})
