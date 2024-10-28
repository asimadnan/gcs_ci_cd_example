import argparse
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import wandb
import joblib
import json
from google.cloud import storage
import os
import tempfile

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--max_depth", type=int, default=3)
    parser.add_argument("--learning_rate", type=float, default=0.1)
    parser.add_argument("--subsample", type=float, default=0.8)
    parser.add_argument("--job_name", type=str, required=True)
    return parser.parse_args()

def load_data():
    data_url = "http://lib.stat.cmu.edu/datasets/boston"
    raw_df = pd.read_csv(data_url, sep="\s+", skiprows=22, header=None)
    data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
    target = raw_df.values[1::2, 2]
    columns = [
        "CRIM", "ZN", "INDUS", "CHAS", "NOX", "RM", "AGE", "DIS", "RAD",
        "TAX", "PTRATIO", "B", "LSTAT"
    ]
    df = pd.DataFrame(data, columns=columns)
    df["MEDV"] = target
    return df

def save_model_to_gcs(bucket_name, model, metrics, job_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Save model
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        joblib.dump(model, temp_file.name)
        temp_file.flush()
        model_blob = bucket.blob(f"{job_name}/model.joblib")
        model_blob.upload_from_filename(temp_file.name)
    os.unlink(temp_file.name)

    # Save metrics
    metrics_blob = bucket.blob(f"{job_name}/metrics.json")
    metrics_blob.upload_from_string(json.dumps(metrics))

def get_best_model_metrics(bucket_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    best_metrics_blob = bucket.blob("best_model/metrics.json")
    
    if best_metrics_blob.exists():
        return json.loads(best_metrics_blob.download_as_string())
    return None

def update_best_model(bucket_name, job_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Copy model
    bucket.copy_blob(bucket.blob(f"{job_name}/model.joblib"), bucket, "best_model/model.joblib")
    
    # Copy metrics
    bucket.copy_blob(bucket.blob(f"{job_name}/metrics.json"), bucket, "best_model/metrics.json")

def main():
    args = parse_args()
    wandb.login(key=os.environ.get("WANDB_API_KEY"))

    # Initialize Weights & Biases logging
    wandb.init(
        project="xgboost-hyperparam-tuning",
        config={
            "n_estimators": args.n_estimators,
            "max_depth": args.max_depth,
            "learning_rate": args.learning_rate,
            "subsample": args.subsample,
        },
    )

    # Load and prepare data
    df = load_data()
    X = df.drop(columns=["MEDV"])
    y = df["MEDV"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Initialize and train model
    model = XGBRegressor(
        n_estimators=args.n_estimators,
        max_depth=args.max_depth,
        learning_rate=args.learning_rate,
        subsample=args.subsample,
    )
    model.fit(X_train, y_train)

    # Calculate metrics
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)

    metrics = {"rmse": rmse, "mse": mse}

    # Log metrics to Weights & Biases
    wandb.log(metrics)

    # Save model and metrics to GCS
    bucket_name = "boston-house-price"  # Replace with your actual bucket name
    save_model_to_gcs(bucket_name, model, metrics, args.job_name)

    # Compare with best model
    best_metrics = get_best_model_metrics(bucket_name)
    if best_metrics is None or metrics["rmse"] < best_metrics["rmse"]:
        update_best_model(bucket_name, args.job_name)
        print("New best model!")
    else:
        print("Current model did not outperform the best model.")

    # Print metrics for logging
    print(f"RMSE: {rmse}")
    print(f"MSE: {mse}")
    print(
        f"Hyperparameters: n_estimators={args.n_estimators}, "
        f"max_depth={args.max_depth}, learning_rate={args.learning_rate}, "
        f"subsample={args.subsample}"
    )

    # Finish the WandB run
    wandb.finish()

if __name__ == "__main__":
    main()