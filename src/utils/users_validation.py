from src.models.users_model import Users
from src.exception.exception import CustomException


# validate the data during the creating users
def user_data_validation(data):
    if not isinstance(data, dict):
        return "Valida json data is required"

    required_fields = [
        "first_name",
        "last_name",
        "email",
        "username",
        "age",
        "gender",
        "password",
    ]

    missing_fields = [
        fields
        for fields in required_fields
        if fields not in data or data[fields] == None or data[fields] == ""
    ]

    if missing_fields:
        return f"Missing required fields:{missing_fields}"

    age = data["age"]
    if age <= 0:
        return "Age must be positive"

    return None


# validate the data during the updation
def update_user_data_validation(data, user):

    if isinstance(data, dict):
        return "Valid json is required"

    allowed_fields = {
        "first_name",
        "middle_name",
        "last_name",
        "email",
        "username",
        "gender",
        "password",
    }

    invalid_fields = set(data.keys()) - allowed_fields

    if invalid_fields:
        return f"Invalid fields: {', '.join(invalid_fields)}"

    # check the provided fields are empty or not
    for field in allowed_fields - {"middle_name"}:
        if field in data and (data[field] is None or data[field] == ""):
            return "Updated fields shouldn't be empty"

    # check the email is already used or not
    if "email" in data:
        existing_email = Users.query.filter(
            Users.email == data["email"], Users.id != user.id
        ).first()

        if existing_email:
            return "Email already exist"

    # check the user is already used or not
    if "username" in data:
        existing_email = Users.query.filter(
            Users.username == data["username"], Users.id != user.id
        ).first()

        if existing_email:
            return "Username already exist"

    return None


# login data validation
def login_validation(data):
    if data == None:
        return "Please enter the require feilds"

    if "password" in data and (data["password"] == "" or data["password"] == None):
        return "Please enter the password"

    if "username" in data and (data["username"] == "" or data["username"] == None):
        return "Please enter the Username"

    return None


# check wheather the data that has been send by user is empty or not
def data_validation(data: dict, feilds: list):
    try:
        for feild in feilds:
            if data[feild] == "" or data[feild] == None:
                return "Required feild is empty"
        return None
    except Exception as e:
        raise CustomException(e)
