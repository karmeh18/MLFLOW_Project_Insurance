import pandas as pd
from src.cloud_storage.aws_storage import AWS_Storage_Service
from botocore.exceptions import ClientError
from src.constants import *
data_pkl = pd.read_pickle(r"D:\Vikash_dash_Demo_Spam_MLOps\MLFLOW_Project_Insurance\data\artifacts\preprocessor\preprocessed_train_data.pkl")

def file_exists(self, s3_path: str) -> bool:
    try:
        self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_path)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        raise


s3 = AWS_Storage_Service(bucket_name=MODEL_BUCKET_NAME)

if not s3.file_exists(AWS_Model_Save):
    raise FileNotFoundError(f"Model key '{AWS_Model_Save}' not found in bucket.")

if not s3.file_exists(AWS_Preprocessor):
    raise FileNotFoundError(f"Preprocessor key '{AWS_Preprocessor}' not found in bucket.")


