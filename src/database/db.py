""" 
Connecting to the database 
"""

from src.exception.exception import CustomException
import os 
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def config_database(app):
    try:
        database_user = os.getenv("DATABASEUSER")
        password = os.getenv("PASSWORD")
        database = os.getenv("DATABASE")
        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{database_user}:{password}@localhost/{database}"
        db.init_app(app)
        with app.app_context():
            print("Database connected successfully")
        
    except Exception as e:
        raise CustomException(e)



def create_table(app):
    try:
        with app.app_context():
            db.create_all()
            print("Table is created")

    except Exception as e:
        raise CustomException(e)