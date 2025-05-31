import os
import pandas as pd
import numpy
from src.configuration.mongo_db_connection import MongoDBClient
from src.data_access.proj1_data import DataCalling
from src.constants import Project_Name, Cluster_Name
from src.logger import logging


data_caller=DataCalling()
df=data_caller.export_collection_as_dataframe()
data_dir="data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
df.to_csv(os.path.join(data_dir, "insurance_data.csv"), index=False)
logging.info(f"data/Data exported to {os.path.join(data_dir, 'insurance_data.csv')} successfully.")