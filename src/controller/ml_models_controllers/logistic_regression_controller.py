from flask import request, jsonify

from src.models.ml_model import TrainedModel
from src.database.db import db
from src.models.users_model import Users
from src.utils.users_validation import data_validation
from src.utils.file_utils import file_validation
from src.utils.ml_utils import save_model, save_preprocessor

from src.config.filepath_config import (
    config_data_filePath,
    config_model_path,
    config_preprocessor_path,
)
from src.utils.file_utils import save_file
from src.ml_models.model_train.LogisticRegression import LoR


def LogisticRegressionController():
    try:
        data = request.form
        file = request.files.get("file")
        data = request.form

        metadata = {
            "C": float(data.get("C", 1.0)),
            "l1_ratio": float(data.get("l1_ratio", 0.0)),
            "class_weight": data.get("class_weight") or None,
            "fit_intercept": data.get("fit_intercept", "true").lower() == "true",
            "solver": data.get("solver", "lbfgs"),
            "max_iter": int(data.get("max_iter", 100)),
            "tol": float(data.get("tol", 0.0001)),
            "random_state": (
                int(data["random_state"]) if data.get("random_state") else None
            ),
            "model_name": data["model_name"],
            "model_creator": data["model_creator"],
            "target_column": data["target_column"],
        }

        require_fields = ["model_creator", "model_name", "target_column"]
        error = data_validation(metadata, require_fields)
        if error:
            return jsonify({"message": error}), 404

        users = Users.query.filter(Users.username == metadata["model_creator"])
        if not users:
            return jsonify({"message": "User is not register"}), 404

        msg, is_error = file_validation(file, metadata["target_column"])
        if is_error:
            return jsonify({"message": msg}), 404

        filepath = config_data_filePath(file.filename, metadata["model_creator"])
        is_saved = save_file(filepath, file)

        preprocessor_filepath = config_preprocessor_path(
            metadata["model_name"], metadata["model_creator"]
        )
        model_filepath = config_model_path(
            metadata["model_name"], metadata["model_creator"]
        )

        lor = LoR(
            C=metadata["C"],
            l1_ratio=metadata["l1_ratio"],
            class_weight=metadata["class_weight"],
            fit_intercept=metadata["fit_intercept"],
            solver=metadata["solver"],
            max_iter=metadata["max_iter"],
            tol=metadata["tol"],
            random_state=metadata["random_state"],
            target_column=metadata["target_column"],
            filepath=filepath,
        )
        performance, model, preprocessor = lor.train_model()
        save_model(model_filepath, model)
        save_preprocessor(preprocessor_filepath, preprocessor)

        newmodel = TrainedModel(
            model_creator=metadata["model_creator"],
            target_column=metadata["target_column"],
            model_metadata=dict(
                {
                    "model_name": metadata["model_name"],
                    "C": metadata["C"],
                    "l1_ratio": metadata["l1_ratio"],
                    "class_weight": metadata["class_weight"],
                    "fit_intercept": metadata["fit_intercept"],
                    "solver": metadata["solver"],
                    "max_iter": metadata["max_iter"],
                    "tol": metadata["tol"],
                    "random_state": metadata["random_state"],
                }
            ),
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
        

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"message": "Something went wrong"}), 500
