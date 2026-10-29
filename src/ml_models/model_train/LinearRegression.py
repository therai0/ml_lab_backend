""" 
Here class are design to train the models
"""

from src.exception.exception import CustomException
import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from src.utils.ml_utils import performance_metrix

class LR:
    def __init__(self, **kwargs):
        self.filepath = kwargs["filepath"]
        self.tolerance = kwargs["tolerance"]
        self.copyX = kwargs["copy_x"]
        self.positive = kwargs["positive"]
        self.fit_intercept = kwargs["fit_intercept"]
        self.target_column = kwargs["target_column"]

    def model_train(self):
        try:
            print(self.target_column)
            model = LinearRegression()
            df = pd.read_csv(self.filepath)
            df.drop(["Unnamed: 0"],axis=1,inplace=True)
            print(df.head())
            X = df.drop([self.target_column],axis=1)
            y = df[self.target_column]
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
            scalar = StandardScaler()
            X_train_scaled = scalar.fit_transform(X_train)
            X_test_scaled = scalar.transform(X_test)

            model.fit(X_train_scaled,y_train)

            y_pred = model.predict(X_test_scaled)

            performance = performance_metrix(y_test,y_pred,is_classification=False)
            return performance
        except Exception as e:
            raise CustomException(e)
        
        
       