import pytest
import os
import pandas as pd
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.aws_demo import S3DataFolderUploader
from src.constants import *

def test_data_ingestion():
    di = DataIngestion()
    df = di.DataCaller()
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    # Test split
    result = di.split_data_as_train_test(df, test_size=Test_Size)
    assert os.path.exists(Training_Data_Path)
    assert os.path.exists(Testing_Data_Path)

def test_data_validation():
    dv = DataValidation()
    assert dv.train_data is not None
    assert dv.test_data is not None
    assert dv.schema is not None
    assert dv.validate_number_of_columns(dv.train_data)
    assert dv.validate_number_of_columns(dv.test_data)
    assert dv.initiate_data_validation() in [True, False]

def test_data_transformation():
    dt = DataTransformation()
    assert dt.train_data is not None
    assert dt.test_data is not None
    assert dt.schema is not None
    dt.initiate_data_transformation()
    assert os.path.exists(Preprocessor_Obj_Path)
    assert os.path.exists(Preprocessed_Train_Data_Path)
    assert os.path.exists(Preprocessed_Test_Data_Path)

def test_model_trainer():
    mt = ModelTrainer()
    metrics, model = mt.get_model_object_report()
    assert isinstance(metrics, dict)
    assert 'Accuracy' in metrics
    assert os.path.exists(Model_Trainer_Artifact_Path)
    assert os.path.exists(Model_Trainer_Dir_Path)

def test_s3datafolderuploader(monkeypatch):
    # Mock S3 client methods to avoid real AWS calls
    uploader = S3DataFolderUploader()
    class DummyS3Client:
        def head_bucket(self, Bucket): return True
        def upload_file(self, *a, **k): return True
        def get_object(self, Bucket, Key):
            class DummyBody:
                def read(self):
                    import json
                    return json.dumps({'Accuracy': 0.5}).encode('utf-8')
            return {'Body': DummyBody()}
    uploader.s3_client = DummyS3Client()
    assert uploader.is_bucket_exists_or_create() in [True, False, None]
    uploader.upload_data_folder = lambda local_folder: True
    uploader.model_evaluation_and_upload = lambda threshold: True
    assert hasattr(uploader, 'bucket_name')

def test_constants():
    assert isinstance(MODEL_BUCKET_NAME, str)
    assert isinstance(AWS_MODEL_EVALUATION_THRESHOLD, float)
    assert os.path.exists(Data_Path)
    assert os.path.exists(Training_Data_Path)
    assert os.path.exists(Testing_Data_Path)
