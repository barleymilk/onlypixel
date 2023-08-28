from sqlalchemy.orm import Session
import models

# 이메일 중복 체크 함수
def check_duplicate_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first() is not None

# 이메일 인증코드, 만료시간 저장 함수
# def temp_code_time(db: Session, )