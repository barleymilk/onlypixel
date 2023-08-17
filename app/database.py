from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import json

# 현재 파일의 절대 경로
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 상위 디렉토리의 절대 경로
PARENT_DIR = os.path.dirname(CURRENT_DIR)

# secrets.json 파일의 경로
SECRETS_FILE_PATH = os.path.join(PARENT_DIR, 'secrets.json')

secrets = json.loads(open(SECRETS_FILE_PATH).read())
SECRET_KEY = secrets["SECRET_KEY"]

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{SECRET_KEY["user"]}:{SECRET_KEY["password"]}@{SECRET_KEY["host"]}:{SECRET_KEY["port"]}/{SECRET_KEY["database"]}?charset=utf8'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

from sqlalchemy.orm import Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()