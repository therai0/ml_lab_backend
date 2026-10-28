from flask import Blueprint

from src.controller.ml_models_controllers.linear_regression_controller import LinearRegressionModel

mlmodel_bp = Blueprint("mlmodel_bp",__name__,url_prefix="/models")

mlmodel_bp.route("/train/linear-regression",methods=["GET","POST"])(LinearRegressionModel)