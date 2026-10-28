from src.constant.constant import BASE_DIR
from src.exception.exception import CustomException
from datetime import datetime

# this function return the file path where file need to save
# it should be in this format => data/username/filename
# filename format => username_filename_current_time.csv(extention can be different)


def configFilePath(filename: str, username: str) -> str:
    try:
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        filename,extension = filename.split(".")
        data_filepath = f"{BASE_DIR}/{username}/data/{username}_{filename}_{current_time}.{extension}"
        return data_filepath
    except Exception as e:
        raise CustomException(e)
