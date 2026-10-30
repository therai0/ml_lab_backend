
from sklearn.linear_model import LogisticRegression 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd 

from src.exception.exception import CustomException
from src.utils.ml_utils import performance_metrix
class LoR:
    def __init__(self, **kwargs):
        self.C = kwargs.get("C", 1.0)
        self.l1_ratio = kwargs.get("l1_ratio", 0.0)
        self.class_weight = kwargs.get("class_weight", None)
        self.fit_intercept = kwargs.get("fit_intercept", True)
        self.solver = kwargs.get("solver", "lbfgs")
        self.max_iter = kwargs.get("max_iter", 100)
        self.tol = kwargs.get("tol", 0.0001)
        self.random_state = kwargs.get("random_state", None)
        self.target_column = kwargs.get("target_column")
        self.filepath= kwargs.get("filepath")

    def train_model(self):
        try:
            df = pd.read_csv(self.filepath)
            model = LogisticRegression(
                C=self.C,
                l1_ratio=self.l1_ratio,
                class_weight=self.class_weight,
                fit_intercept=self.fit_intercept,
                solver=self.solver,
                max_iter=self.max_iter,
                tol=self.tol,
                random_state=self.random_state
            )
            X = df.drop([self.target_column],axis=1)
            y = df[self.target_column]
            X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
            scalar=StandardScaler()
            X_train_scaled = scalar.fit_transform(X_train)
            X_test_scaled = scalar.transform(X_test)

            model.fit(X_train_scaled,y_train)
            y_pred = model.predict(X_test_scaled)
            performance = performance_metrix(y_test,y_pred,is_classification=True)
            return performance,model,scalar
        except Exception as e:
            print(e)
            raise CustomException(e)