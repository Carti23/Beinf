"""
S3 utility module for handling AWS S3 operations with LocalStack.

Dependencies:
    - boto3: AWS SDK for S3 operations
    - os: For environment variable access
"""

import boto3
import os

# Initialize S3 client with LocalStack configuration
s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("LOCALSTACK_S3_ENDPOINT", "http://localhost:4566"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
)

BUCKET_NAME = "my-bucket"

# Create S3 bucket
s3.create_bucket(Bucket=BUCKET_NAME)

def upload_file_to_s3(file_path, file_name):
    """
    Upload a file to S3 bucket.
    
    Args:
        file_path (str): Path to the local file
        file_name (str): Name for the file in S3
        
    Returns:
        str: S3 URI of the uploaded file
    """
    s3.upload_file(file_path, BUCKET_NAME, file_name)
    return f"s3://{BUCKET_NAME}/{file_name}"

def download_file_from_s3(file_name, local_path):
    """
    Download a file from S3 bucket.
    
    Args:
        file_name (str): Name of the file in S3
        local_path (str): Path where to save the file locally
    """
    s3.download_file(BUCKET_NAME, file_name, local_path)