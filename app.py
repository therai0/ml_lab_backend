import os
from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

from src.database.db import config_database, create_table
from src.models.users_model import Users
from src.exception.exception import CustomException

# routes
from src.routes.user_routes import user_bp
from src.routes.ml_routes import mlmodel_bp


load_dotenv()

def create_app():
    try:
        app = Flask(__name__)
        CORS(app)
        app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
        app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)
        app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
        app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
        app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token"

        JWTManager(app)
        config_database(app)
        create_table(app)
        app.register_blueprint(user_bp)
        app.register_blueprint(mlmodel_bp)
        return app
    except Exception as e:
        raise CustomException(e)


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8000)
