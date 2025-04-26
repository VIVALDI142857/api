import grpc
import predict_pb2
import predict_pb2_grpc
import json
import pandas as pd

def run_from_str():
    # Создаем канал связи с сервером
    channel = grpc.insecure_channel('grpc:50051')
    
    # Создаем stub
    stub = predict_pb2_grpc.PredictorStub(channel)

    # Пример данных в формате JSON (имитируем строку с данными)
    data = pd.read_csv('../api_dfs/X_test.csv').to_json(orient='records')

    
    # Создаем запрос
    request = predict_pb2.StrRequest(json_data=data)

    # Отправляем запрос и получаем ответ
    response = stub.PredictFromStr(request)

    # Выводим результат
    print("Response from server:")
    print(response.predictions_json)

if __name__ == '__main__':
    run_from_str()
    
    
    
