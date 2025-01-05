# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set environment variables for SageMaker paths
ENV PYTHONUNBUFFERED=TRUE
ENV PATH="/opt/program:${PATH}"
ENV PYTHONPATH="/opt/program:${PYTHONPATH}"

# Set the working directory inside the container
WORKDIR /opt/program

# Install any required system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your inference script and other necessary files into the container
COPY inference.py /opt/program/inference.py

# Create the directory for model artifacts
RUN mkdir -p /opt/ml/model

# Expose the port used by the Flask app (if using Flask)
EXPOSE 8080

# Set the entry point script for SageMaker Inference
ENTRYPOINT ["python", "inference.py"]
