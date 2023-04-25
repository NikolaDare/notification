from .database import Base
from sqlalchemy import Text,TIMESTAMP, Column, String, Boolean,Integer,DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship,Mapped,mapped_column
from sqlalchemy.sql import func
from typing import List, Union

class User(Base):
    __tablename__ = 'user'
    id = Column('user_id', Integer, primary_key=True)
    email = Column(String(255))
    name= Column(String(255))
    lastName= Column(String(255))
    appSettings= Column(Text,default=['[]'])
    role_id: Mapped[int] = mapped_column(ForeignKey("role.role_id"),default=2)
    children: Mapped[List["Token"]] = relationship()
    notifications: Mapped[List["Notifications"]] = relationship()
class Token(Base):
    __tablename__='token'
    id = Column('token_id', Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    expires=Column('expires',String(100) )
    external_key=Column('external_key',Text)
    internal_key=Column('internal_key',Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
   
class Role(Base):
    __tablename__='role'
    id = Column('role_id', Integer, primary_key=True)
    name=Column('role_name',String(100) )
    children: Mapped[List["User"]] = relationship()
    
class Notifications(Base):
    __tablename__='notification'
    id = Column('noti_id', Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    text=Column('noti_body',Text)
    apps_id: Mapped[int] = mapped_column(ForeignKey("apps.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    
class Apps(Base):
    __tablename__='apps'
    id = Column('id', Integer, primary_key=True)
    name=Column('name',String(100) )
    path=Column('path',String(255) ) 
    icon=Column('icon',String(100) )
    children: Mapped[List["Notifications"]] = relationship()
    

