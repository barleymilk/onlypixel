import datetime
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
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="../templates")

db_dependency = Annotated[Session, Depends(main_crud.get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

## 커뮤니티페이지
@router.get("/", status_code=status.HTTP_200_OK)
async def posts(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse("posts.html", {"request": request})

## 커뮤니티 게시판 페이지
@router.get("/{post_menu}", status_code=status.HTTP_200_OK)
async def read_post_menu(post_menu: int = Path(gt=0)):
    return {"post-menu": post_menu}

## 커뮤니티 단일 페이지
@router.get("/{post_menu}/{post_id}", status_code=status.HTTP_200_OK)
async def read_one_post(post_menu, post_id: int = Path(gt=0)):
    return {"post-menu": post_menu, "post-id": post_id}

# 글 작성
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_post(user: user_dependency):
    return {"message": "포스트 작성 완료"}

# 글 수정(본인, 로그인)
# @app.put("/posts/{post_menu}/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_post(user: user_dependency,
                      post_request: schemas.PostRequest, 
                      post_id: int = Path(gt=0),
                      db: Session=Depends(main_crud.get_db)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    post_changed = False
    post_model = db.query(models.Post).filter(models.Post.id == post_id)
    if post_model is None:
        raise HTTPException(status_code=404, detail='없는 포스트입니다.')
    else:
        post_model.post_menu = post_request.post_menu
        post_model.title = post_request.title
        post_model.content = post_request.content
        post_model.last_modified_date = datetime.datetime.now()
        post_model.image_path = post_request.image_path
        post_model.video_path = post_request.video_path
        post_changed = True
    
    if not post_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "포스트 내용 수정"}

# 글 삭제(본인, 로그인)
@router.delete("/{post_menu}/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(user: user_dependency, 
                      post_menu, post_id: int = Path(gt=0),
                      db: Session=Depends(main_crud.get_db)):
    post_changed = False
    post_model = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post_model is None:
        raise HTTPException(status_code=404, detail='없는 포스트입니다.')
    else:
        db.query(models.Post).filter(models.Post.id == post_id).delete()
        db.commit()
        post_changed = True
    if not post_changed:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "포스트 삭제"}