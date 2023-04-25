from sqlalchemy.orm import Session

from . import models

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_key_from_user(db: Session, user_id: int):
    return db.query(models.Token).filter(models.Token.user_id == user_id).first()

def get_notifications_from_user(db: Session, user_id: int):
    return db.query(models.Notifications).filter(models.Notifications.user_id == user_id).all()

# def get_roles(db: Session):
#     return db.query(models.Role).all()

def create_user(db: Session, user: dict):
    db_user = models.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_token(db: Session, token: dict, user_id: int):
    token.update({'user_id':user_id})
    db_item = models.Item(**token)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_notifications(db: Session, noti: dict, user_id: int,app_id:int):
    noti.update({'user_id':user_id,'app_id':app_id})
    db_noti = models.Notifications(**noti)
    db.add(db_noti)
    db.commit()
    db.refresh(db_noti)
    return db_noti