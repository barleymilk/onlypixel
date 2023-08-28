import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from starlette import status
from starlette.responses import RedirectResponse

from fastapi import Depends, APIRouter, Path, Request, Form
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
    prefix="/mini-games",
    tags=["mini-games"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")

db_dependency = Annotated[Session, Depends(main_crud.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

## 미니게임 페이지
@router.get("/", status_code=status.HTTP_200_OK)
async def mini_games(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("mini_games.html", {"request": request})