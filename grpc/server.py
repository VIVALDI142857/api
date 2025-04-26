import grpc
from concurrent import futures
import predict_pb2
import predict_pb2_grpc
import pandas as pd
import json
import mlflow.pyfunc

mlflow.set_tracking_uri("http://hostname123.zapto.org:5000")
logged_model = 'runs:/4c85ecd0b1dc41f78f2d6b9dc33095cb/model_pipeline'
model = mlflow.pyfunc.load_model(logged_model)

class PredictorServicer(predict_pb2_grpc.PredictorServicer):
    def PredictFromFile(self, request, context):
        import io
        df = pd.read_csv(io.BytesIO(request.csv_file))
        preds = model.predict(df)
        print("Predictions:", preds)  #
        return predict_pb2.PredictResponse(predictions_json=pd.DataFrame(preds).to_json(orient="records"))

    def PredictFromStr(self, request, context):
        df = pd.read_json(request.json_data)
        preds = model.predict(df)
        return predict_pb2.PredictResponse(predictions_json=pd.DataFrame(preds).to_json(orient="records"))

    def PredictEachCol(self, request, context):
        rows = [vars(r) for r in request.data]
        df = pd.DataFrame(rows)
        preds = model.predict(df)
        return predict_pb2.PredictResponse(predictions_json=pd.DataFrame(preds).to_json())

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    predict_pb2_grpc.add_PredictorServicer_to_server(PredictorServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("gRPC server is running at port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
