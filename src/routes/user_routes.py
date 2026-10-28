from flask import Blueprint 
from src.controller.user_controller import (Create_user,
                                            Update_user_data,
                                            get_user,
                                            login,
                                            test)

# creating blueprint
user_bp = Blueprint("users", __name__,url_prefix="/api/auth")

# user route [create,update,login,logout]
user_bp.route("/create_user",methods=["POST","GET"])(Create_user)
user_bp.route("/update/<int:user_id>",methods=["POST","GET"])(Update_user_data)
user_bp.route("/<int:user_id>",methods=["GET"])(get_user)
user_bp.route("/login",methods=["POST"])(login)
user_bp.route("/test",methods=["POST","GET"])(test)









