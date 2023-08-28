import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# 전체 건수, 페이징 적용된 게임 목록
def get_games_list(db: Session, skip: int = 0, limit: int = 0):
    _games_list = db.query(models.Game).order_by(models.Game.release_date.desc())
    total = _games_list.count()
    games_list = _games_list.offset(skip).limit(limit).all()
    return total, games_list