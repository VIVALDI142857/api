from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, ConfigDict, Field
import pandas as pd
import numpy as np
from typing import List
from time import sleep
import json
import xgboost
import catboost
import pandas as pd
import numpy as np
import sklearn 
from catboost import CatBoostClassifier
from xgboost import XGBClassifier
import mlflow
import mlflow.sklearn
from fastapi import FastAPI
import mlflow.pyfunc
from pydantic import BaseModel


app = FastAPI()

import mlflow
mlflow.set_tracking_uri("http://hostname123.zapto.org:5000")

logged_model = 'runs:/4c85ecd0b1dc41f78f2d6b9dc33095cb/model_pipeline'

model = mlflow.pyfunc.load_model(logged_model)

class Df_str(BaseModel):
    data: str
    
class Row(BaseModel):

    Followers: int
    Following: int
    Posts: int
    Bio: int
    profile_picture: int
    external_link: int
    mutual_friends: int
    Threads: int
    Following_Followers: float
    Posts_Followers: float
        
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


    
    
    
    

    