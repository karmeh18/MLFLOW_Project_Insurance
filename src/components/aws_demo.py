import boto3
import os
import pickle
from io import StringIO
import json
from botocore.exceptions import ClientError
from src.configuration.aws_connection import S3Connection
from src.cloud_storage.aws_storage import AWS_Storage_Service
from src.constants import *
from src.logger import logging

class S3DataFolderUploader:
    def __init__(self, bucket_name=None):
        
        s3_connection = S3Connection()
        self.s3_client = s3_connection.s3_client
        #self.bucket_name = bucket_name if bucket_name else MODEL_BUCKET_NAME
        self.s3_resource = s3_connection.s3_resource
        self.bucket_name = MODEL_BUCKET_NAME
        self.old_model_artifact = Model_Trainer_Artifact_Path
        self.old_model_path = Model_Trainer_Dir_Path
        self.data_path = Data_Path
        self.training_data_path = Training_Data_Path
        self.test_data_path = Testing_Data_Path
        self.preprocessor = Preprocessor_Obj_Path
        self.train_preprocessor = Preprocessed_Train_Data_Path
        self.test_preprocessor = Preprocessed_Test_Data_Path
        self.data_validation_report = Data_Validation_Report_Path
        self.aws_model_path = AWS_Model_Save
        self.aws_model_artifact = AWS_Model_Artifact



    def is_bucket_exists_or_create(self):
        """
        Checks if the S3 bucket exists. If not, creates it and returns False (indicating it was just created).
        Returns True if the bucket already existed, False if it was just created.
        """
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logging.info(f"Bucket '{self.bucket_name}' exists.")
            return True  # Already existed
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404' or error_code == 'NoSuchBucket':
                logging.warning(f"Bucket '{self.bucket_name}' does not exist. Creating bucket...")
                try:
                    if self.s3_client.meta.region_name == 'us-east-1':
                        self.s3_client.create_bucket(Bucket=self.bucket_name)
                    else:
                        self.s3_client.create_bucket(
                            Bucket=self.bucket_name,
                            CreateBucketConfiguration={'LocationConstraint': self.s3_client.meta.region_name}
                        )
                    logging.info(f"Bucket '{self.bucket_name}' created successfully.")
                    self.upload_data_folder(local_folder="data")
                    logging.info(f"Data folder uploaded to bucket '{self.bucket_name}'.")
                    return False  # Just created
                except Exception as ce:
                    logging.error(f"Failed to create bucket '{self.bucket_name}': {ce}")
                    return None
            else:
                raise e

    def upload_data_folder(self, local_folder="data"):
        """
        Upload all files from the specified local 'data' folder to the S3 bucket, preserving folder structure.
        """
        for root, _, files in os.walk(local_folder):
            for file in files:
                local_path = os.path.join(root, file)
                # S3 key should be relative to the data folder, but keep 'data/' as the prefix in S3
                s3_key = os.path.relpath(local_path, os.path.dirname(local_folder)).replace('\\', '/')
                self.s3_client.upload_file(local_path, self.bucket_name, s3_key)
                logging.info(f"Uploaded {local_path} to s3://{self.bucket_name}/{s3_key}")

    def model_evaluation_and_upload(self,threshold):
        """
        Compare new model accuracy (from local artifact) with old accuracy (from S3).
        If improved by at least `threshold`, upload the data folder to S3.
        """
        import tempfile
        local_artifact_path = os.path.join("data", "artifacts", "Model", "Model_Artifact.json")
        s3_artifact_key = local_artifact_path.replace("\\", "/")

        # Load new model accuracy from local artifact
        try:
            with open(local_artifact_path, "r") as f:
                new_artifact = json.load(f)
                new_accuracy = new_artifact.get("Accuracy")
        except Exception as e:
            logging.error(f"Failed to read local model artifact: {e}")
            return

        # Try to fetch old model accuracy from S3 (read directly, no download)
        old_accuracy = None
        try:
            s3_obj = self.s3_client.get_object(Bucket=self.bucket_name, Key=s3_artifact_key)
            old_artifact = json.load(s3_obj['Body'])
            old_accuracy = old_artifact.get("Accuracy")
        except self.s3_client.exceptions.NoSuchKey:
            logging.warning(f"No previous model artifact found in S3 at {s3_artifact_key}. Treating as no previous model.")
        except Exception as e:
            logging.warning(f"Could not fetch old model artifact from S3: {e}")

        # If no old accuracy, treat as always improved
        if old_accuracy is None:
            improved = True
        else:
            improved = (new_accuracy is not None and old_accuracy is not None and (new_accuracy - old_accuracy) >= AWS_MODEL_EVALUATION_THRESHOLD)

        if improved:
            logging.info(f"New model accuracy ({new_accuracy}) improved over old ({old_accuracy}). Uploading data folder.")
            self.upload_data_folder(local_folder="data")
        else:
            logging.info(f"New model accuracy ({new_accuracy}) did not improve by threshold ({AWS_MODEL_EVALUATION_THRESHOLD}) over old ({old_accuracy}). No upload performed.")
