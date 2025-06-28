import boto3
import os
import pickle
from io import StringIO
import pandas as pd
import json
from botocore.exceptions import ClientError
from src.configuration.aws_connection import S3Connection
from src.constants import *
from src.logger import logging

class AWS_Storage_Service:
    """
    A Class for interacting with AWS S3 storage, providing methods for file management, data uploads and data retrieval in S3 buckets.
    """

    def __init__(self, bucket_name=None):
        s3_connection = S3Connection()
        self.s3_resource = s3_connection.s3_resource
        self.s3_client = s3_connection.s3_client
        self.bucket_name = bucket_name if bucket_name else MODEL_BUCKET_NAME

    def create_bucket(self, bucket_name=None, region=REGION):
        """
        Create an S3 bucket in a specified region.
        :param bucket_name: Name of the bucket to create. Defaults to the instance's bucket_name.
        :param region: AWS region. Defaults to REGION from constants.
        """
        bucket_name = bucket_name if bucket_name else self.bucket_name
        try:
            if region == 'us-east-1':
                response = self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                response = self.s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            logging.info(f"✅ Bucket '{bucket_name}' created successfully.")
            return response
        except Exception as e:
            logging.error(f"❌ Failed to create bucket: {e}")
            raise e


    def upload_file(self, file_path: str, s3_path: str) -> None:
        """Upload a file from the local filesystem to the specified S3 bucket."""
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_path)
            logging.info(f"Uploaded {file_path} to s3://{self.bucket_name}/{s3_path}")
        except ClientError as e:
            logging.error(f"Failed to upload {file_path} to S3: {e}")
            raise e
        
    def get_object(self, s3_path: str):
        response = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_path)
        return response['Body'].read()

    def file_exists(self, s3_path: str) -> bool:
        """Check if a file exists in the S3 bucket."""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise

    def download_file(self, file_path: str, s3_path: str) -> None:
        """Download a file from S3 to the local filesystem."""
        try:
            self.s3_client.download_file(self.bucket_name, s3_path, file_path)
            logging.info(f"Downloaded s3://{self.bucket_name}/{s3_path} to {file_path}")
        except ClientError as e:
            logging.error(f"Failed to download {s3_path} from S3: {e}")
            raise e

    def list_files(self, prefix: str = "") -> list:
        """List files in the S3 bucket under a given prefix."""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            files = [item['Key'] for item in response.get('Contents', [])]
            logging.info(f"Files in s3://{self.bucket_name}/{prefix}: {files}")
            return files
        except ClientError as e:
            logging.error(f"Failed to list files in S3: {e}")
            return []

    def upload_project_folder(self, local_folder: str, s3_prefix: str = "") -> None:
        """Recursively upload all files from a local folder to S3, preserving the folder structure."""
        for root, _, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_folder)
                s3_key = os.path.join(s3_prefix, relative_path).replace("\\", "/")
                self.upload_file(local_path, s3_key)

    def download_project_folder(self, s3_prefix: str, local_folder: str) -> None:
        """Download all files from an S3 prefix to a local folder, preserving the folder structure."""
        files = self.list_files(s3_prefix)
        for s3_key in files:
            relative_path = os.path.relpath(s3_key, s3_prefix)
            local_path = os.path.join(local_folder, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            self.download_file(s3_key, local_path)

# s3_conn = S3Connection()
# s3_client = s3_conn.s3_client
# key = AWS_Model_Artifact

# # Get the object from S3
# response = s3_client.get_object(Bucket=MODEL_BUCKET_NAME, Key=key)
# content = json.loads(response['Body'].read().decode('utf-8'))

# # Handle both 'accuracy' and 'Accuracy' keys
# accuracy = content.get('accuracy', content.get('Accuracy'))
# print(f"Accuracy: {accuracy}")


#content = response['Body'].read().decode('utf-8')
#print(content)
# aws_service.upload_file(Data_Path,AWS_Data_file_path)
# aws_service.upload_file(Training_Data_Path,AWS_Split_Data_path_Training)
# aws_service.upload_file(Testing_Data_Path,AWS_Split_Data_path_Testing)
# aws_service.upload_file(Model_Trainer_Dir_Path, AWS_Model_Save)
# aws_service.upload_file(Model_Trainer_Artifact_Path,AWS_Model_Artifact)
# aws_service.list_files("project_data/")