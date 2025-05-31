import os
from datetime import datetime

Project_Name = "MLOPS_Insurance_Data"
Cluster_Name = "ClusterMLOPSINSURANCE"
Data_Path = r"data\insurance_data.csv"
Artifact_Dir = "data/artifacts"
Split_Data = "data/artifacts/Split_Data"
Training_Data_Path = r"data\artifacts\Split_Data\training_data.csv"
Testing_Data_Path = r"data\artifacts\Split_Data\testing_data.csv"
Test_Size= 0.2
Random_State = 42