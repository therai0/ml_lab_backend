""" 
All the file related methods are here
saving file
deleting file
validation file type
check null value or not 
file is encoded or not.
"""
import os 
import pandas as pd 
from src.exception.exception import CustomException

def save_file(file_path:str,file):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        file.save(file_path)

        if os.path.isfile(file_path):
            return True
        return False
    except Exception as e:
        CustomException(e)


def file_validation(file):
    if not file:
        return "File is not provided",False 

    # check file type
    if not file.filename.lower().endswith("csv"):
        return "Only CSV file are allowed",False 

    # check the file size
    file.seek(0,2)
    file_size = file.tell()
    file.seek(0)
    MAX_SIZE = 1024*1024
    if file_size > MAX_SIZE:
        return "File size must not exceed 1MB",True 

    # Read and validate CSV
    try:
        df = pd.read_csv(file)
        file.seek(0)  # Important: reset after reading

    except pd.errors.EmptyDataError:
        file.seek(0)
        return "CSV file is empty", True

    except pd.errors.ParserError:
        file.seek(0)
        return "Invalid CSV format", True

    # Check for null values
    if df.isnull().any().any():
        return "Null values are not allowed", True

    # Check for non-numeric columns
    if not all(
        pd.api.types.is_numeric_dtype(dtype)
        for dtype in df.dtypes
    ):
        return "Only encoded/numeric columns are accepted", True

    return "", False

    

    



