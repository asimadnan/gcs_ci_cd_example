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