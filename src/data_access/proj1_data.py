import sys
import os
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBClient
from src.constants import Project_Name, Cluster_Name
from src.logger import logging
from dotenv import load_dotenv
load_dotenv()
load_data=os.getenv('data_url')
url=os.getenv("Connection_url")

class DataCalling:
    def __init__(self) -> None:
        try:
            logging.info("Establishing Connection with MongoDB")
            self.mongo_client = MongoDBClient(Project_Name, Cluster_Name)
        except Exception as e:
            logging.exception(f"❌ Error initializing MongoDB client: {e}")

    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        Export a MongoDB collection to a Pandas DataFrame.
        :return: DataFrame containing the collection data.
        """
        try:
            if self.mongo_client.database is None:
                print("❌ No database connection found")
                return pd.DataFrame()
            else:
                collection = self.mongo_client.collection
                logging.info("Connection Established with MongoDB")
                data = list(collection.find())
                print(f"✅ Data fetched with the length of {len(data)}")

                df = pd.DataFrame(data)
                if "_id" in df.columns:
                    df.drop(columns=["_id","id"], inplace=True)
                df.replace({np.nan: None}, inplace=True)
                return df

        except Exception as e:
            logging.exception(f"❌ Error exporting collection to DataFrame: {e}")
            return pd.DataFrame()  # return empty on error

# DC = DataCalling()
# DC.export_collection_as_dataframe()