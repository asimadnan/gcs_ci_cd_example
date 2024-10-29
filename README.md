# CI/CD Pipeline for ML Model Training and Deployment on GCP

CI/CD pipeline repository for deploying a machine learning model on Google Cloud Platform (GCP)! This project (attempts to) automates model training, validation, and deployment using GitHub Actions, Docker, Google Cloud Run, and Weights & Biases for experiment tracking. 

## Repository Structure

The repo is organized as below

- `.github/workflows/ci-cd-pipeline.yaml`: Contains the GitHub Actions workflow that defines the CI/CD pipeline steps.
- `Dockerfile`: Containerizes the environment for both training and serving the model.
- `entrypoint.sh`: Intended to handle either training or serving depending on the input arguments.
- `main.py`, `training.py`: Core scripts for training and handling ML processes.
- `requirements.txt`: Lists dependencies.
- `tests/`: Contains test scripts to validate the model's performance.
- `wandb/`: Set up for experiment logging and tracking.

  
## Pipeline Overview

This CI/CD pipeline automatically triggers on every `push` to the main branch or when a pull request is made. Here’s a high-level flow of how it works:

1. **Environment Setup**: The pipeline starts by setting up Python and installing dependencies.

2. **Docker Build and Push**: 
   - Builds a Docker image and pushes it to Google Artifact Registry. This image is configured for both training and serving, though currently only training is fully operational.

3. **Model Training on GCP**:
   - A Cloud Run job is created or updated to handle the model training process.
   - Weights & Biases API is configured for logging and tracking experiment metrics.
   - The trained model artifact is saved to Google Cloud Storage, specifically if it outperforms any previous model saved in `gs://boston-house-price/best_model`.

4. **Validation and Conditional Deployment**:
   - After training, the pipeline checks if the new model is the best based on metrics.
   - If it’s the best model, the pipeline proceeds to deploy the Docker container to Cloud Run to serve predictions.
  
5. **Testing the Deployed Model**: 
   - Sends a request to the Cloud Run endpoint to verify that predictions are returned as expected.

6. **Error Handling and Logs**:
   - In case of failures, the pipeline retrieves logs from the Cloud Run service for debugging.

## Learning and Observations

This project was my first experience with Google Cloud, specifically with Cloud Run and Vertex AI. Here’s a breakdown of what I learned and challenges faced:

1. **Training and Serving in the Same Container**:
   - The Docker image is designed to handle both training and serving, controlled via the `entrypoint.sh` script. While this has worked well in AWS with the same setup, I ran into issues on GCP.
   - I attempted deploying this on Cloud Run, but the serving endpoint failed to start, even though training executed and saved the model artifact as intended. Running a Flask server in Cloud Run proved tricky, and I couldn’t get it working with this configuration.
   - for some reason cloud run just doesn't want to run, even when i simply try to replace docker file with a sample from https://github.com/GoogleCloudPlatform/cloud-run-samples/blob/main/README.md and simple flask server. So I just give up for now.

2. **Exploring Google Vertex AI**:
   - I also tried deploying the model via Vertex AI by registering each model and deploying it as an endpoint. However, I found Vertex AI endpoints to be slower than expected, which impacted usability for quick iteration and testing.

3. **Next Steps**:
   - This project served as a first attempt at deploying a model on GCP. I plan to revisit this pipeline to further streamline the setup, potentially separating training and serving processes for more stability.
   - Simplifying deployment and improving response times for serving models are key focus areas for future improvements.

## Future Improvements

Some ideas for improvement include:
- **Optimizing Docker Image for Separate Training and Serving**: This could resolve the Cloud Run serving issues.
- **Experimenting with Other GCP Services**: Possibly Cloud Functions for lightweight models or Vertex AI for managed deployments, despite its latency.
- **Enhanced Error Logging and Monitoring**: Adding more granular logging to troubleshoot Cloud Run failures effectively.

This repository provides a CI/CD framework that showcases the foundational setup for ML model automation on GCP, despite the challenges faced. Feel free to experiment and modify the pipeline to meet your specific needs!


















## Adding required Permissions

```
gcloud projects add-iam-policy-binding boston-house-price-439411 --member="serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding boston-house-price-439411 --member="serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding boston-house-price-439411 --member="serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com" --role="roles/iam.serviceAccountUser"


gcloud iam service-accounts keys create key.json --iam-account=github-actions@boston-house-price-439411.iam.gserviceaccount.com


gcloud projects add-iam-policy-binding boston-house-price-439411 \
  --member=serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com \
  --role=roles/artifactregistry.writer

  gcloud services enable artifactregistry.googleapis.com

  gcloud projects add-iam-policy-binding boston-house-price-439411 \
  --member=serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com \
  --role=roles/storage.admin

  gcloud projects add-iam-policy-binding boston-house-price-439411 \
  --member=serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com \
  --role=roles/artifactregistry.admin

  gcloud artifacts repositories create ml-models \
  --repository-format=docker \
  --location=us-central1 \
  --description="ML models repository"

  gcloud artifacts repositories create ml-models --repository-format=docker --location=uaustralia-southeast1 --description="ML models repository"

gcloud projects add-iam-policy-binding boston-house-price-439411 \
  --member=serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com \
  --role=roles/artifactregistry.admin

  gcloud projects add-iam-policy-binding boston-house-price-439411 \
  --member=serviceAccount:github-actions@boston-house-price-439411.iam.gserviceaccount.com \
  --role=roles/storage.admin


export PROJECT_ID="boston-house-price-439411"
export REGION="australia-southeast1"
export IMAGE_URI="australia-southeast1-docker.pkg.dev/$PROJECT_ID/ml-models/ml-model:latest"
export SERVICE_NAME="ml-model-service"docker push $IMAGE_URI

export GCS_BUCKET_NAME="boston-house-price"
export MODEL_PATH="best_model/model.joblib"
```