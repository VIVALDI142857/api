import requests
import pandas as pd
from fastapi import FastAPI
import mlflow.sklearn
from pydantic import BaseModel
import uvicorn
from fastapi import HTTPException
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, roc_curve, fbeta_score, precision_recall_curve, average_precision_score, balanced_accuracy_score

mlflow.set_tracking_uri(mlflow.set_tracking_uri("http://192.168.1.104:5000"))

X_test = pd.read_csv('api_dfs/X_test.csv')
y_test = pd.read_csv('api_dfs/y_test.csv')


model = mlflow.sklearn.load_model(f"models:/CatBoostClassifier/2")

predictions = model.predict(X_test)
f1 = f1_score(y_test, predictions, average='weighted')
accuracy = accuracy_score(y_test, predictions)
fbeta = fbeta_score(y_test, predictions, beta=1.5)
b_acc = balanced_accuracy_score(y_test, predictions)

metrics = {'f1': f1,   
           'accuracy': accuracy,
           'fbeta': fbeta,
           'b_acc': b_acc
}

app = FastAPI()
    
    
@app.get("/", tags=['Status'], summary='get server status')
def home():
    return {"message": "FastAPI is running!"}

@app.get('/clients', tags=['Data'], summary='print the df')
def get_df():
    return X_test

@app.get('/learning', tags=['Learning'], summary='get model prediction results.')
def get_metrics():
    return metrics

@app.get('/clients/{id}', tags=['Data'], summary='Get info about a client')
def get_client(id: int):
    if id not in X_test.index:
        raise HTTPException(status_code=404)
    return X_test[X_test.index == id]
