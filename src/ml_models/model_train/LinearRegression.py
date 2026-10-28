""" 
Here class are design to train the models
"""

from src.exception.exception import CustomException
import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error,mean_squared_error,root_mean_squared_error

class LR:
    def __init__(self, **kwargs):
        self.file = kwargs["file"]
        self.tolerance = kwargs["tolerance"]
        self.copyX = kwargs["copyX"]
        self.positive = kwargs["positive"]
        self.fitintercept = kwargs["fitintercept"]
        self.is_scaled =kwargs["is_scaled"]

    def model_train(self):
        try:
            model = LinearRegression()
            df = pd.read_csv(self.file)
            scalar = StandardScaler()
            

        except Exception as e:
            raise CustomException(e)
        
        
       