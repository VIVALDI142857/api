import mlflow.sklearn
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, ConfigDict, Field
import pandas as pd
import numpy as np
import re
from typing import List
from time import sleep
import json

app = FastAPI()

model = mlflow.sklearn.load_model('./mlruns/583777404083659989/29c546b38411430399e68c8485b9fac0/artifacts/model_pipeline')

class Df_str(BaseModel):
    data: str
    
class Row(BaseModel):

    id: float
    fea_1: float
    fea_2: float
    fea_3: float
    fea_4: float
    fea_5: float
    fea_6: float
    fea_7: float
    fea_8: float
    fea_9: float
    fea_10: float
    fea_11: float
    OVD_t1_mean: float
    OVD_t1_max: float
    OVD_t2_mean: float
    OVD_t2_max: float
    OVD_t3_mean: float
    OVD_t3_max: float
    pay_normal_mean: float
    pay_normal_max: float
    prod_code_median: float
    update_date_mean: float
    report_date_mean: float
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
    return res.to_json()

@app.post('/predict_str')
async def predict_str(df_str: Df_str):
    X = pd.read_json(df_str.data)
    res = model.predict(X)
    res = pd.DataFrame(res)
    return res.to_json()

@app.post('/predict_each_col')
async def predict_each(data: Dataframe):
    # X = pd.read_json(pd.read_json(data.model_dump_json())['data'].to_list())
    X = pd.DataFrame.from_dict(json.loads(data.model_dump_json())['data'])
    # print(str(X['data'])[:100])
    # sleep(5)
    res = model.predict(X)
    res = pd.DataFrame(res)
    return res.to_json()


    
    
    
    

    