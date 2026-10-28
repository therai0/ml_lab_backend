from src.database.db import db 
from sqlalchemy.orm import Mapped,mapped_column 
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import String,Integer,func,DateTime
from datetime import datetime

""" 
Model for creating user account 
"""
class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
    middle_name:Mapped[str] = mapped_column(String(50),nullable=True)
    first_name:Mapped[str] = mapped_column(String(50),nullable=False)
    last_name:Mapped[str] = mapped_column(String(50),nullable=False)
    email:Mapped[str] = mapped_column(String(100),nullable=False,unique=True)
    username:Mapped[str] = mapped_column(String(20),unique=True,nullable=False)
    age:Mapped[int] = mapped_column(nullable=False)
    gender:Mapped[str]= mapped_column(String(20),nullable=False)
    password:Mapped[str] = mapped_column(String(200),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),nullable=False)
    updated_at:Mapped[datetime] = mapped_column( DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

