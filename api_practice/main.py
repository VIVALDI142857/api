from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, ConfigDict, Field
import pandas as pd
import numpy as np
import re
from typing import List
from time import sleep
import json
import xgboost
import catboost
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sc
from ydata_profiling import ProfileReport
from scipy import stats as sts
import sklearn 
from sklearn.preprocessing import PowerTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
pd.set_option('display.max_columns', None)
from sklearn.impute import SimpleImputer, KNNImputer
sklearn.impute.KNNImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, roc_curve, fbeta_score, precision_recall_curve, average_precision_score, balanced_accuracy_score
from sklearn.model_selection import train_test_split
import phik
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
import mlflow
import mlflow.sklearn  # Если нужно логировать модели sklearn
import os
from mlflow.models import infer_signature
import optuna
from fastapi import FastAPI
import mlflow.pyfunc
from pydantic import BaseModel


app = FastAPI()

import mlflow
mlflow.set_tracking_uri("http://hostname123.zapto.org:5000")


logged_model = 'runs:/671a6251d94b4237b8500f80b43ed800/model_pipeline'

model = mlflow.pyfunc.load_model(logged_model)

class Df_str(BaseModel):
    data: str
    
class Row(BaseModel):

    fea_1: int
    fea_2: float
    fea_3: int
    fea_4: float
    fea_5: int
    fea_6: int
    fea_7: int
    fea_8: int
    fea_9: int
    fea_10: int
    fea_11: float
    OVD_t1_mean: float
    OVD_t1_max: int
    OVD_t2_mean: float
    OVD_t2_max: int
    OVD_t3_mean: float
    OVD_t3_max: int
    pay_normal_mean: float
    pay_normal_max: int
    prod_code_median: float
    update_date_mean: int
    report_date_mean: int
    prod_limit_mean: float
    new_balance_mean: float
    highest_balance_mean: float
    
class Dataframe(BaseModel):
    data: List[Row] = Field(..., description='')
 
@app.post('/predict_file')
async def predict_file(file: UploadFile = File(...)):
    X = pd.read_csv(file.file)
    res = model.predict(X)
    res = pd.DataFrame(res)
    return res.to_json(orient='records')

@app.post('/predict_str')
async def predict_str(df_str: Df_str):
    X = pd.read_json(df_str.data)
    res = model.predict(X)
    res = pd.DataFrame(res)
    return res.to_json(orient='records')

@app.post('/predict_each_col')
async def predict_each(data: Dataframe):
    X = pd.DataFrame.from_dict(json.loads(data.model_dump_json())['data'])
    res = model.predict(X)
    res = pd.DataFrame(res)
    return res.to_json()


    
    
    
    

    