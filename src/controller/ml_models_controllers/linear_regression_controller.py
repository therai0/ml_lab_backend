from flask import request, jsonify
import pandas as pd 
from src.database.db import db
from src.models.users_model import Users
from src.utils.users_validation import data_validation
from src.config.filepath_config import configFilePath
from src.utils.file_utils import save_file
from src.utils.file_utils import file_validation


def LinearRegressionModel():
    try:
        data = request.form
        file = request.files.get("file")
        model_data = {
            "model_name":data.get("modelname"),
            "model_creator":data.get("username"),
            "copyX":data.get("copyX"),
            "tolerance":data.get("tolerance"),
            "positive":data.get("positive"),
            "fitintercept":data.get("fitintercept"),
        }
        require_feilds = ["model_name","model_creator"]
        
        # check weather the inputs feilds are empty or not
        error = data_validation(model_data,require_feilds)
        if error:
            return jsonify({
                "message":error 
            }),404
        
        # check wheather the user is valid user or not
        users = Users.query.filter(Users.username== model_data["model_creator"])
        if not users:
            return jsonify({
                "message":"User is not register"
            }),404

        # if the file is not valid
        msg,is_error = file_validation(file)
        if  is_error:
            return jsonify({
                    "message":msg
            }),404
        
        filepath = configFilePath(file.filename,model_data["model_creator"])
        is_saved= save_file(filepath,file)
        if is_saved:
            df = pd.read_csv(filepath)
            print(df.shape)

        return jsonify({"messagge": "I got the data"}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "Something went wrong"}), 500
