import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from sqlalchemy.orm import Session
from database import SessionLocal
import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_games(db: Session, limit: int = None):
    query = db.query(models.Game)
    if limit is not None:
        query = query.limit(limit)
    return query.all()

def get_news(db: Session, limit: int = None):
    query = db.query(models.News)
    if limit is not None:
        query = query.limit(limit)
    return query.all()