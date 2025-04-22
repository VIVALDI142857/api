import streamlit as st
import os 
import pandas as pd
import requests
import mlflow
import json
from sklearn.metrics import f1_score

base_url = 'http://fastapi:'


df = None
file = None
# url = os.getenv('URL')

st.title('Hello')
file = st.file_uploader('Upload your file', type=['csv', 'xls', 'xlsx'])
if file:
    if file.name.endswith('csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
        
        

    st.dataframe(df)
    st.write(df)

if st.sidebar.button('predict'):
    if file:
        url = f'{base_url}/predict_file'
        response = requests.post(url, files={"file": ("data.csv", df.to_csv(index=False), "text/csv")})

        if response.status_code == 200:
            json_data = response.json()
            pred = pd.read_json(json_data)
            st.download_button('download csv', data=pred.to_csv(index=False), file_name='preds.csv', mime='text/csv')

          