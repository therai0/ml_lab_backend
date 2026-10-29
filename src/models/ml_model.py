""" 
All the classes design here are for database table
"""

from src.database.db import db 
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String,Integer,func,DateTime
from datetime import datetime

class LinearRegressionModel(db.Model):
    model_id:Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
    model_createor:Mapped[String] = mapped_column(String(255),nullable=False)
    njobs:Mapped[bool]= mapped_column(bool,nullable=False)
    model_name:Mapped[String] = mapped_column(String(255),nullable=False)
    filename:Mapped[String]= mapped_column(String(255),nullable=False)
    filepath:Mapped[String] = mapped_column(String(255),nullable=False)
    copyx:Mapped[bool] = mapped_column(bool,nullable=False)
    tolerance:Mapped[String]=mapped_column(String(255),nullable=False)
    positive:Mapped[bool]=mapped_column(bool,nullable=False)
    create_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),nullable=False)
