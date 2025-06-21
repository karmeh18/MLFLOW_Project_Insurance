import os
from datetime import datetime

Project_Name = "MLOPS_Insurance_Data"
Cluster_Name = "ClusterMLOPSINSURANCE"
Data_Path = r"data\insurance_data.csv"
Data_Dir="data"
Artifact_Dir = "data/artifacts"
Split_Data = "data/artifacts/Split_Data"

Training_Data_Path = r"data\artifacts\Split_Data\training_data.csv"
Testing_Data_Path = r"data\artifacts\Split_Data\testing_data.csv"
Test_Size= 0.2
Random_State = 42

Schema_Yaml_File_Path = "config/schema.yaml"
Model_Yaml_File_Path = "config/model.yaml"
Data_Validation_Report_Path = r"data\artifacts\Validation_Report\report.json"

Preprocessor_Obj_Path = "data/artifacts/preprocessor/preprocessor.pkl"
Preprocessed_Train_Data_Path = "data/artifacts/preprocessor/preprocessed_train_data.pkl"
Preprocessed_Test_Data_Path = "data/artifacts/preprocessor/preprocessed_test_data.pkl"


#Model Trainer
Model_Trainer_Dir_Path = "data/artifacts/Model/rfc.pkl"
Model_Trainer_Expected_Score: float = 0.6
Model_Trainer_N_Estimator: int = 200
Model_Trainer_Min_Sample_Split: int = 7
Model_Trainer_Min_Sample_Leaf: int = 6
Min_Sample_Split_Max_Depth: int = 10
Min_Sample_Split_Criterion: str = 'entropy'
Min_Sample_Split_Random_State: int = 101

#Model Metrics
Model_Trainer_Artifact_Path = "data/artifacts/Model/Model_Artifact.json"


#AWS 
REGION = "us-east-1"
AWS_MODEL_EVALUATION_THRESHOLD = 0.02
MODEL_BUCKET_NAME = "insurancebucketproj"
AWS_Data_file_path = "project_data/insurance_data.csv"
AWS_Split_Data_path_Training = "project_data/Artifacts/Split_Data/training_data.csv"
AWS_Split_Data_path_Testing = "project_data/Artifacts/Split_Data/testing_data.csv"
AWS_Preprocess_Train_Data = "project_data/Artifacts/preprocessed_train_data.pkl"
AWS_Preprocess_Test_Data = "project_data/Artifacts/preprocessed_test_data.pkl"
AWS_Preprocessor = "project_data/Artifacts/preprocessor.pkl"
AWS_Validation_Report = "project_data/Artifacts/Validation_Report/report.json"
AWS_Model_Save = "project_data/Artifacts/Model/rfc.pkl"
AWS_Model_Artifact = "project_data/Artifacts/Model/Model_Artifact.json"


#APP Deployment
APP_HOST = "0.0.0.0"
APP_PORT = 5000

