import os
import pandas as pd
import numpy as np
from src.configuration.mongo_db_connection import MongoDBClient
from src.data_access.proj1_data import DataCalling
from src.constants import *
from src.logger import logging
from src.constants import *
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
load_data=os.getenv('data_url')
url=os.getenv("Connection_url")

class DataIngestion:
    
    def DataCaller(self) -> pd.DataFrame:
        """
        Fetch data from MongoDB and return it as a DataFrame.
        :return: DataFrame containing the collection data.
        """
        try:
            logging.info("Starting data Importing from MongoDB")
            data_caller = DataCalling()
            df = data_caller.export_collection_as_dataframe()
            if not os.path.exists(Data_Dir):
                os.makedirs(Data_Dir)
                df.to_csv(os.path.join(Data_Dir, "insurance_data.csv"), index=False)
            logging.info(f"Data exported to {os.path.join(Data_Dir, 'insurance_data.csv')} successfully.")
            if df.empty:
                logging.warning("No data found in the collection.")
            else:
                logging.info(f"Data fetched successfully with {len(df)} records.")
            return df
        except Exception as e:
            logging.exception(f"Error during data ingestion: {e}")
        return pd.DataFrame()
        
    def split_data_as_train_test(self, df: pd.DataFrame, test_size: float) -> None:
        """
        Split the DataFrame into training and testing sets.
        :param df: DataFrame to be split.
        :param test_size: Proportion of the dataset to include in the test split.
        """
        try:
            logging.info("Starting data splitting into train and test sets")
            train_set , test_set = train_test_split(df, test_size=Test_Size, random_state=Random_State)
            logging.info("Performed train test split on the data frame")
            os.makedirs(Artifact_Dir,exist_ok=True)
            os.makedirs(Split_Data, exist_ok=True)
            logging.info(f"Train and test data split Started")
            train_set.to_csv(Training_Data_Path, index=False)
            test_set.to_csv(Testing_Data_Path, index=False)

            logging.info(f"Exported and Saved train and test file path")
        except Exception as e:
            logging.exception(f"Error during data splitting: {e}")

    def initiate_data_ingestion(self) -> None:
        """
        Initiate the data ingestion process.
        """
        try:
            df = self.DataCaller()
            logging.info("Data Reading has been started")
            #df=pd.read_csv(Data_Path)
            return self.split_data_as_train_test(df, Test_Size)
        except Exception as e:
            logging.exception(f"Error in data ingestion pipeline: {e}")

            
#DataIngestion().initiate_data_ingestion()