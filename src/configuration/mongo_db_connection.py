import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

from src.logger import logging

# Load environment variables
load_dotenv()
ca = certifi.where()


class MongoDBClient:
    client = None  # class-level shared client

    def __init__(self, project_name: str, cluster_name: str) -> None:
        try:
            if MongoDBClient.client is None:
                url = os.getenv("Connection_url")
                MongoDBClient.client = MongoClient(url, tlsCAFile=ca)

            self.client = MongoDBClient.client
            self.project_name = project_name
            self.database = self.client[project_name]
            self.collection = self.database[cluster_name]
            logging.debug("Connection Successful")

        except Exception as e:
            logging.exception("❌ Error connecting to MongoDB")
        


