import gradio as gr
import pandas as pd
import requests
import io

base_url = 'http://localhost:9123'

def predict(file):
    filename = file.name
    if filename.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    url = f'{base_url}/predict_file'
    response = requests.post(url=url, files={'file':('data.csv', df.to_csv(index=False), 'text/csv')})

    if response.status_code == 200:
        json_data = response.json()

        df_pred = pd.read_csv(io.StringIO(json_data))
        return df_pred


def export_csv(dataframe, *args):
    filename = "predictions.csv"
    dataframe.to_csv(filename, index=False)
    return gr.File(value=filename, visible=True) 

with gr.Blocks() as demo:
    with gr.Row():
        upload = gr.File(label="Upload CSV/Excel", file_types=[".csv", ".xls", ".xlsx"])
        df_output = gr.Dataframe()
        
        with gr.Column():
            export_btn = gr.Button("Export to CSV")
            download = gr.File(interactive=False, visible=False)
    
    upload.change(predict, upload, df_output)
    export_btn.click(export_csv, inputs=[df_output, download], outputs=download)

demo.launch(server_name="0.0.0.0", server_port=8543)
