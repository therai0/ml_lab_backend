import traceback
import os


class CustomException(Exception):
    def __init__(self, error: Exception):
        tb = traceback.extract_tb(error.__traceback__)[-1]

        self.error_message = str(error)
        self.line_no = tb.lineno
        self.file_name = os.path.basename(tb.filename)
        self.page_name = tb.name

    def __str__(self):
        return (
            f"Error: {self.error_message}\n"
            f"File: {self.file_name}\n"
            f"Line: {self.line_no}\n"
            f"Page/Function: {self.page_name}"
        )