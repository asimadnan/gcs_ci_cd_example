import os
from flask import Flask, request, jsonify
import joblib
from google.cloud import storage

app = Flask(__name__)

# Load the model at startup
storage_client = storage.Client()
bucket = storage_client.bucket("boston-house-price")
blob = bucket.blob("best_model/model.joblib")
model = joblib.load(blob.download_as_bytes())


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    prediction = model.predict([data["features"]])
    return jsonify({"prediction": prediction.tolist()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
