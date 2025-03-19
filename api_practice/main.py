import mlflow.sklearn
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, ConfigDict
import pandas as pd
import numpy as np

app = FastAPI()

model = mlflow.sklearn.load_model('/home/vivaldi/MyProjects/ssh_first_try/mlruns/583777404083659989/29c546b38411430399e68c8485b9fac0/artifacts/model_pipeline')

app.state.preds = []
 
    
@app.post('/predict', summary='prediction')
async def predict(file: UploadFile = File(...)):
    X = pd.read_csv(file.file)
    app.state.preds = model.predict(X).tolist()
    return({'predictions': preds})

@app.get('/predictions')
def get_preds():
    return({'predictions': app.state.preds})


    
    
    
    

    