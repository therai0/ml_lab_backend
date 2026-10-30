""" 
All the classes design here are for database table
"""

from src.database.db import db 
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,func,DateTime,JSON,ForeignKey
from datetime import datetime

class TrainedModel(db.Model):
    __tablename__ = "trained_models"
    model_id:Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
    model_creator:Mapped[String] = mapped_column(String(255),ForeignKey('users.username'),nullable=False)
    target_column:Mapped[String] = mapped_column(String(255),nullable=False)
    model_metadata:Mapped[dict] = mapped_column(JSON,nullable=False)
    model_performance:Mapped[dict] = mapped_column(JSON,nullable=False)
    data_filepath:Mapped[String] = mapped_column(String(255),nullable=False)
    model_filepath:Mapped[String] = mapped_column(String(255),nullable=False)
    preprocessor_filepath:Mapped[String] = mapped_column(String(255),nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=func.now(),nullable=False)

