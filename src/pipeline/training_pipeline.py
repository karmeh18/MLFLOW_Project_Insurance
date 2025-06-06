from src.components.data_ingestion import DataIngestion
from src.logger import logging
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer


class TrainingPipeline:        
    def start(self) -> None:
        try:
            print("------------------------------------Data Inestion--------------------------------------")
            logging.info("Data Ingestion Pipeline Started")
            self.data_ingestion = DataIngestion()
            self.data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed successfully.")
            print("------------------------------------Data Validation--------------------------------------")
            self.data_validation = DataValidation()
            logging.info("Data Validation Pipeline Initialized")
            self.data_validation.initiate_data_validation()
            logging.info("Data Validation Pipeline Completed")
            print("------------------------------------Data Transformation--------------------------------------")
            self.data_transformation = DataTransformation()
            logging.info("Data Transformation Pipeline Initialized")
            self.data_transformation.initiate_data_transformation()
            logging.info("Data Transformation Pipeline Completed")
            print("------------------------------------Model Trainer--------------------------------------")
            self.model_trainer=ModelTrainer()
            logging.info("Model Training has been Initialized")
            self.model_trainer.initiate_model_training()
            logging.info("Model Training Pipeline has been Completed")
            


        except Exception as e:
            print(f"An error occurred during the training pipeline: {e}")

pipeline=TrainingPipeline()
pipeline.start()