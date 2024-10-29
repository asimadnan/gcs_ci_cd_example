# # Use Python 3.8 slim image
# FROM python:3.8-slim

# # Set working directory
# WORKDIR /app

# # Copy and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY . .

# # Set the required environment variables for Cloud Run
# ENV PORT=8080
# ENV FLASK_RUN_PORT=8080

# # Expose the port that Flask will use
# EXPOSE 8080

# # Set the default command for training or serving
# CMD ["python", "predict.py"]
# Use python as base image
FROM python:3.6-stretch

# Use working directory /app/model
WORKDIR /app/model

# Copy and install required packages
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy all the content of current directory to working directory
COPY . .

# Set env variables for Cloud Run
ENV PORT 80
ENV HOST 0.0.0.0

EXPOSE 80:80

# Run flask app
CMD ["python", "app.py"]