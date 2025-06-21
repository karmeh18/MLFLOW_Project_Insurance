import os
from src.constants import MODEL_BUCKET_NAME, REGION, AWS_Model_Save
from src.logger import logging
from src.cloud_storage.aws_storage import AWS_Storage_Service
from botocore.exceptions import ClientError

import os
import boto3
from botocore.exceptions import ClientError

class S3ModelUploader:
    def __init__(self):
        self.bucket_name = MODEL_BUCKET_NAME
        self.region = REGION
        self.s3_client = boto3.client("s3", region_name=REGION)


    def model_exists(self, s3_key=AWS_Model_Save) -> bool:
        """Check if a model file already exists in the S3 bucket."""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            print(f"☑️ Model already exists in S3: {s3_key}")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            raise Exception(f"❌ Error checking model existence: {e}")

    def upload_model(self, local_model_path: str, s3_key: str):
        """Upload the model to S3 if it doesn't already exist."""
        self.create_bucket_if_not_exists()
        if self.model_exists(s3_key):
            print("ℹ️ Skipping upload. Model already exists.")
            return

        try:
            self.s3_client.upload_file(local_model_path, self.bucket_name, s3_key)
            print(f"✅ Model uploaded to s3://{self.bucket_name}/{s3_key}")
        except ClientError as e:
            raise Exception(f"❌ Failed to upload model: {e}")
