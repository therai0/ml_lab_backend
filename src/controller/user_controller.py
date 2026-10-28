from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    jwt_required
)
from datetime import timedelta
from src.exception.exception import CustomException
from src.utils.users_validation import (
    user_data_validation,
    update_user_data_validation,
    login_validation,
)
from src.models.users_model import Users
from src.database.db import db


# method help to create the user account
def Create_user():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        error = user_data_validation(data)
        if error:
            return jsonify({"success": False, "message": error}), 400

        new_user = Users(
            first_name=data["first_name"],
            middle_name=data.get("middle_name") or None,
            last_name=data["last_name"],
            email=data["email"],
            username=data["username"],
            age=int(data["age"]),
            gender=data["gender"],
            password=generate_password_hash(data["password"]),
        )

        db.session.add(new_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "User created successfully",
                    "user": {
                        "id": new_user.id,
                        "first_name": new_user.first_name,
                        "last_name": new_user.last_name,
                        "email": new_user.email,
                        "username": new_user.username,
                    },
                }
            ),
            201,
        )
    except Exception as e:
        # if the some error occures in database it should not commit and rollback to previous state
        db.session.rollback()
        CustomException(e)
        return jsonify({"success": False, "message": "Something went wrong"}), 500


# this method helps to update the user data except the user passsword(seperate method is there to update the password of uesrs)
@jwt_required()
def Update_user_data(user_id):
    try:
        update_user_fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "username",
            "gender",
        ]
        data = request.get_json()
        if not user_id:
            return jsonify({"success": False, "message": "User id is required"}), 400

        # read the data from the database of particular user
        user = db.session.get(Users, user_id)

        if not user:
            return jsonify({"success": False, "message": "User not found"}), 404

        error = update_user_data_validation(data, user)
        if error:
            return jsonify({"success": False, "message": error}), 400

        for field in update_user_fields:
            if field in data:
                setattr(user, field, data[field])

        # save the change
        db.session.commit()
        return jsonify({"success": True, "message": "Updated data successfully"}), 200

    except Exception as e:
        db.session.rollback()
        CustomException(e)
        return jsonify({"success": False, "message": "Something went wrong"}), 500


# read the user data of particular id
@jwt_required()
def get_user(user_id):
    try:
        if not user_id:
            return jsonify({"success": False, "message": "User id is required"}), 400

        user = db.session.get(Users, user_id)
        # only the data which are need to response
        res_user_data = {
            "username": user.username,
            "age": user.age,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "middle_name": user.middle_name,
            "join_date": user.created_at,
            "gender": user.gender,
        }
        return jsonify({"success": True, "data": res_user_data}), 200

    except Exception as e:
        print(e)
        CustomException(e)
        return jsonify({"success": False, "message": "Something went wrong"}), 500


# method for loggin
def login():
    try:
        data = request.get_json()
        print(data)
        error = login_validation(data)
        if error:
            return jsonify({"success": False, "message": error}), 404

        user = Users.query.filter(Users.username == data["username"]).first()

        if not user or (not check_password_hash(user.password, data["password"])):
            return jsonify(
                {"success": False, "message": "Invalid username or password"}
            ),404

        access_token = create_access_token(
            identity=user.username, expires_delta=timedelta(hours=1)
        )
        refresh_token = create_refresh_token(
            identity=user.username, expires_delta=timedelta(days=1)
        )
        response = jsonify(
                {
                    "success": True,
                    "message": "Login successfully",
                    "data":{
                        "username":user.username
                    }
                }
            )

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response

    except Exception as e:
        # raise CustomException(e)
        print(e)
        return jsonify({"success": False, "message": "Something went wrong"}), 500


# decorator to protect the route 
@jwt_required()
def test():
    return jsonify({"message": "everything is fine its working"})


# methods to logout the users
@jwt_required()
def logout():
    try:
        response = jsonify({
            "success":True,
            "message":"Logout successfully"
        }) 
    except Exception as e:
        print(e)
        return jsonify({
            "success":False,
            "message":"Something went wrong"
        }),500
    