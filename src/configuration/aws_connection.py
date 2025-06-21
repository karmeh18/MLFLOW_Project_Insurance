import boto3
import os
from src.constants import REGION
from src.logger import logging
from dotenv import load_dotenv
load_dotenv()

class S3Connection:
    s3_client = None
    s3_resource = None

    def __init__(self):
        logging.info("Access to AWS Connection started")
        if S3Connection.s3_client is None or S3Connection.s3_resource is None:
            access_key = os.getenv("AWS_Access_Key")
            secret_key = os.getenv("AWS_Access_Key_Password")
            if not access_key:
                raise Exception("Environment Variable: AWS_Access_Key is not set")
            if not secret_key:
                raise Exception("Environment Variable: AWS_Access_Key_Password is not set")
            S3Connection.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=REGION
            )
            S3Connection.s3_client = boto3.client(
                's3',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=REGION
            )
        self.s3_resource = S3Connection.s3_resource
        self.s3_client = S3Connection.s3_client
        logging.info("Connection to AWS has been established")