from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.components.data_validation import DataValidation


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
    def start(self) -> None:
        try:
            logging.info("Data Ingestion Pipeline Started")
            self.data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully.")
            self.data_validation = DataValidation()
            logging.info("Data Validation Pipeline Initialized")
            self.data_validation.initiate_data_validation()
            logging.info("Data Validation Pipeline Started")

        except Exception as e:
            print(f"An error occurred during the training pipeline: {e}")

pipeline=TrainingPipeline()
pipeline.start()