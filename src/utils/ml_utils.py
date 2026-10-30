
import os 
import pickle
from src.exception.exception import CustomException
from sklearn.metrics import (
    # Regression metrics
    mean_absolute_error,
    mean_squared_error,
    root_mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
    explained_variance_score,
    max_error,
    median_absolute_error,

    # Classification metrics
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    log_loss,
    matthews_corrcoef,
    cohen_kappa_score,
    balanced_accuracy_score,
    jaccard_score,
)


# function to calculate the performance metrix of model
def performance_metrix(y, y_pred, is_classification: bool):
    if is_classification:
        return {
            "accuracy": float(accuracy_score(y, y_pred)),
            "balanced_accuracy": float(balanced_accuracy_score(y, y_pred)),
            "precision": float(
                precision_score(y, y_pred, average="weighted", zero_division=0)
            ),
            "recall": float(
                recall_score(y, y_pred, average="weighted", zero_division=0)
            ),
            "f1_score": float(
                f1_score(y, y_pred, average="weighted", zero_division=0)
            ),
            "jaccard_score": float(
                jaccard_score(y, y_pred, average="weighted", zero_division=0)
            ),
            "matthews_corrcoef": float(matthews_corrcoef(y, y_pred)),
            "cohen_kappa": float(cohen_kappa_score(y, y_pred)),
            "confusion_matrix": confusion_matrix(y, y_pred).tolist(),
            "classification_report": classification_report(
                y, y_pred, output_dict=True, zero_division=0
            ),
        }

    else:
        return {
            "mean_absolute_error": float(mean_absolute_error(y, y_pred)),
            "mean_squared_error": float(mean_squared_error(y, y_pred)),
            "root_mean_squared_error": float(root_mean_squared_error(y, y_pred)),
            "median_absolute_error": float(median_absolute_error(y, y_pred)),
            "r2_score": float(r2_score(y, y_pred)),
            "explained_variance": float(explained_variance_score(y, y_pred)),
            "max_error": float(max_error(y, y_pred)),
            "mean_absolute_percentage_error": float(
                mean_absolute_percentage_error(y, y_pred)
            ),
        }



# function to save the ml model
def save_model(filepath,model):
    try:
        # Create directory if it doesn't exist
        file_dir = os.path.dirname(filepath)

        if file_dir:
            os.makedirs(file_dir, exist_ok=True)

        # Save model
        with open(filepath, "wb") as file:
            pickle.dump(model, file)
        return True

    except Exception as e:
        raise CustomException(f"Failed to save model: {str(e)}")



# function to save the preprocessor file
def save_preprocessor(filepath: str, preprocessor):
    try:
        file_dir = os.path.dirname(filepath)

        if file_dir:
            os.makedirs(file_dir, exist_ok=True)

        with open(filepath, "wb") as file:
            pickle.dump(preprocessor, file)

        return True

    except Exception as e:
        raise Exception(f"Failed to save preprocessor: {str(e)}")