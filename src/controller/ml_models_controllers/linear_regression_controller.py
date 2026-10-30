from flask import request, jsonify

from src.ml_models.model_train.LinearRegression import LR 
from src.database.db import db
from src.models.users_model import Users
from src.models.ml_model import TrainedModel
from src.utils.users_validation import data_validation
from src.config.filepath_config import (
    config_data_filePath,
    config_model_path,
    config_preprocessor_path,
)
from src.utils.file_utils import save_file
from src.utils.file_utils import file_validation
from src.utils.ml_utils import save_model, save_preprocessor

from src.exception.exception import CustomException


def LinearRegressionModelController():
    try:
        data = request.form
        file = request.files.get("file")
        metadata = {
            "model_name": data.get("modelname"),
            "model_creator": data.get("username"),
            "copy_x": data.get("copy_x"),
            "tolerance": data.get("tolerance"),
            "positive": data.get("positive"),
            "fit_intercept": data.get("fit_intercept"),
            "target_column": data.get("target_column"),
        }
        require_feilds = ["model_name", "model_creator"]

        # check weather the inputs feilds are empty or not
        error = data_validation(metadata, require_feilds)
        if error:
            return jsonify({"message": error}), 404

        # check wheather the user is valid user or not
        users = Users.query.filter(Users.username == metadata["model_creator"])
        if not users:
            return jsonify({"message": "User is not register"}), 404

        # check the file is not valid
        msg, is_error = file_validation(file, metadata["target_column"])
        if is_error:
            return jsonify({"message": msg}), 404

        # get the file path[ it return the file path where file will be saved]
        filepath = config_data_filePath(file.filename, metadata["model_creator"])
        # saving the file
        is_saved = save_file(filepath, file)
        preprocessor_filepath = config_preprocessor_path(
            metadata["model_name"], metadata["model_creator"]
        )
        model_filepath = config_model_path(
            metadata["model_name"], metadata["model_creator"]
        )
        if is_saved:
            lr = LR(
                filepath=filepath,
                tolerance=metadata["tolerance"],
                copy_x=metadata["copy_x"],
                positive=metadata["positive"],
                fit_intercept=metadata["fit_intercept"],
                target_column=metadata["target_column"],
            )
            performance, preprocessor, model = lr.model_train()
            save_model(model_filepath, model)
            save_preprocessor(preprocessor_filepath, preprocessor)

            newmodel = TrainedModel(
                model_creator=metadata["model_creator"],
                model_metadata=dict(
                    {
                        "model_name": metadata["model_name"],
                        "copy_x": metadata["copy_x"],
                        "tolerance": metadata["tolerance"],
                        "positive": metadata["positive"],
                        "fit_intercept": metadata["fit_intercept"],
                    }
                ),
                target_column=metadata["target_column"],
                model_performance=performance,
                data_filepath=filepath,
                model_filepath=model_filepath,
                preprocessor_filepath=preprocessor_filepath,
            )
            db.session.add(newmodel)
            db.session.commit()
            return jsonify(
                    {
                        "model_metadata": {
                            "model_name": metadata["model_name"],
                            "model_creator": metadata["model_creator"],
                        },
                        "model_performance": performance,
                    }
                ),200
            

        return jsonify({"messagge": "I got the data"}), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message": "Something went wrong"}), 500
