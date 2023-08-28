import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import SessionLocal
import models

# 전체 건수, 페이징 적용된 뉴스 목록
def get_news_list(db: Session, skip: int = 0, limit: int = 0):
    _news_list = db.query(models.News).order_by(models.News.written_date.desc())
    total = _news_list.count()
    news_list = _news_list.offset(skip).limit(limit).all()
    return total, news_list