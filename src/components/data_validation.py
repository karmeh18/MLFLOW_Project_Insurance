import pandas as pd
import numpy as np
import json
from src.logger import logging
from src.utils.main_utils import *
from src.constants import *

class DataValidation:
    def __init__(self):
        try:
            self.schema=read_yaml(Schema_Yaml_File_Path)
            self.train_data=pd.read_csv(Training_Data_Path)
            self.test_data=pd.read_csv(Testing_Data_Path)
        except Exception as e:
            logging.exception(f"Error initializing DataValidation: {e}")
            raise e
    def validate_number_of_columns(self, df: pd.DataFrame) -> bool:
        """
        Validate the number of columns in the DataFrame.
        :param df: DataFrame to validate.
        :return: True if the number of columns matches the schema, False otherwise.
        """
        try:
            status=len(df.columns) == len(self.schema['columns'])
            logging.info(f"Number of columns validation status: {status}")
            return status
        except Exception as e:
            logging.exception(f"Error validating number of columns: {e}")

    def is_column_exist(self, df: pd.DataFrame) -> bool:
        """
        Check if all columns in the schema exist in the DataFrame.
        :param df: DataFrame to check.
        :return: True if all columns exist, False otherwise.
        """
        try:
            dataframe_columns = df.columns.tolist()
            missing_numerical_columns=[]
            missing_categorical_columns=[]
            for column in self.schema['numerical_columns']:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns) > 0:
                logging.warning(f"Missing numerical columns: {missing_numerical_columns}")
            
            for column in self.schema['categorical_columns']:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns) > 0:
                logging.warning(f"Missing categorical columns: {missing_categorical_columns}")

            return False if len(missing_numerical_columns) > 0 or len(missing_categorical_columns) > 0 else True
        except Exception as e:
            logging.exception(f"Error checking column existence: {e}")
            return False

            
    def initiate_data_validation(self) -> bool:
        """
        Initiate the data validation process.
        :return: True if validation passes, False otherwise.
        """
        try:
            logging.info("Starting data validation")
            train_status = self.validate_number_of_columns(self.train_data)
            test_status = self.validate_number_of_columns(self.test_data)
            if not train_status or not test_status:
                logging.error("Data validation failed: Number of columns mismatch")
                return False

            train_column_status = self.is_column_exist(self.train_data)
            test_column_status = self.is_column_exist(self.test_data)
            if not train_column_status or not test_column_status:
                logging.error("Data validation failed: Missing columns in train or test data")
                return False
            
            logging.info("Data validation passed successfully")

            report_dir = Data_Validation_Report_Path
            os.makedirs(os.path.dirname(report_dir), exist_ok=True)

            logging.info("Saving data validation report")
            report__file={
                "train_data_validation": train_column_status,
                "test_data_validation": test_column_status,
                "train_data_columns": self.train_data.columns.tolist(),
                "test_data_columns": self.test_data.columns.tolist(),
                "Numerical_Columns": self.schema['numerical_columns'],
                "Categorical_Columns": self.schema['categorical_columns'],
            }
            with open(Data_Validation_Report_Path,"w") as file:
                json.dump(report__file, file, indent=4)
            logging.info(f"Data validation report saved at {Data_Validation_Report_Path}")
            return 
        except Exception as e:
            logging.exception(f"Error during data validation: {e}")
            return False
        


#DataValidation().initiate_data_validation()