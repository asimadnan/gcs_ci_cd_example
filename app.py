import os
from flask import Flask, request, jsonify
import joblib
from google.cloud import storage
import json
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    """ Main page of the app. """
    return "Hello World!"




@app.get("/predict")
async def predict(url: str):
    # Load the model at startup
    storage_client = storage.Client()
    bucket = storage_client.bucket("boston-house-price")
    blob = bucket.blob("best_model/model.joblib")
    model = joblib.load(blob.download_as_bytes())
    data = request.json
    prediction = model.predict([data["features"]])
    return jsonify({"prediction": prediction.tolist()})


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
