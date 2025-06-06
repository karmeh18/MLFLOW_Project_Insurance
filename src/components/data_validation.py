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

    def is_column_exist(self, df: pd.DataFrame) -> (bool, str):
        """
        Check if all columns in the schema exist in the DataFrame.
        :param df: DataFrame to check.
        :return: (True/False, message) tuple
        """
        try:
            dataframe_columns = df.columns.tolist()
            missing_numerical_columns = []
            missing_categorical_columns = []
            message = ""
            for column in self.schema['numerical_columns']:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)
            for column in self.schema['categorical_columns']:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)
            if missing_numerical_columns or missing_categorical_columns:
                msg_parts = []
                if missing_numerical_columns:
                    msg_parts.append(f"Missing numerical columns: {missing_numerical_columns}")
                if missing_categorical_columns:
                    msg_parts.append(f"Missing categorical columns: {missing_categorical_columns}")
                message = ", ".join(msg_parts)
                logging.warning(message)
                return False, message
            else:
                message = "All required columns exist in the DataFrame."
                return True, message
        except Exception as e:
            logging.exception(f"Error checking column existence: {e}")
            return False, f"Error checking column existence: {e}"

    def initiate_data_validation(self) -> bool:
        """
        Initiate the data validation process.
        :return: True if validation passes, False otherwise.
        """
        try:
            logging.info("Starting data validation")
            train_status = self.validate_number_of_columns(self.train_data)
            test_status = self.validate_number_of_columns(self.test_data)
            message = ""
            if train_status and test_status:
                message = "Number of columns matches the schema for both train and test data."
            else:
                if not train_status and not test_status:
                    message = "Number of columns does not match the schema for both train and test data."
                elif not train_status:
                    message = "Number of columns does not match the schema for train data."
                elif not test_status:
                    message = "Number of columns does not match the schema for test data."
                logging.error("Data validation failed: Number of columns mismatch")
                report_dir = Data_Validation_Report_Path
                os.makedirs(os.path.dirname(report_dir), exist_ok=True)
                report__file = {
                    "train_data_validation": train_status,
                    "test_data_validation": test_status,
                    "train_data_columns": self.train_data.columns.tolist(),
                    "test_data_columns": self.test_data.columns.tolist(),
                    "Numerical_Columns": self.schema['numerical_columns'],
                    "Categorical_Columns": self.schema['categorical_columns'],
                    "Message": message
                }
                with open(Data_Validation_Report_Path, "w") as file:
                    json.dump(report__file, file, indent=4)
                return False

            train_column_status, train_col_msg = self.is_column_exist(self.train_data)
            test_column_status, test_col_msg = self.is_column_exist(self.test_data)
            if not train_column_status or not test_column_status:
                message = f"{train_col_msg} {'; ' if train_col_msg and test_col_msg else ''}{test_col_msg}"
                logging.error("Data validation failed: Missing columns in train or test data")
                report_dir = Data_Validation_Report_Path
                os.makedirs(os.path.dirname(report_dir), exist_ok=True)
                report__file = {
                    "train_data_validation": train_column_status,
                    "test_data_validation": test_column_status,
                    "train_data_columns": self.train_data.columns.tolist(),
                    "test_data_columns": self.test_data.columns.tolist(),
                    "Numerical_Columns": self.schema['numerical_columns'],
                    "Categorical_Columns": self.schema['categorical_columns'],
                    "Message": message
                }
                with open(Data_Validation_Report_Path, "w") as file:
                    json.dump(report__file, file, indent=4)
                return False

            message = "Data validation passed successfully. All columns exist and number of columns match the schema."
            logging.info(message)
            report_dir = Data_Validation_Report_Path
            os.makedirs(os.path.dirname(report_dir), exist_ok=True)
            report__file = {
                "train_data_validation": train_column_status,
                "test_data_validation": test_column_status,
                "train_data_columns": self.train_data.columns.tolist(),
                "test_data_columns": self.test_data.columns.tolist(),
                "Numerical_Columns": self.schema['numerical_columns'],
                "Categorical_Columns": self.schema['categorical_columns'],
                "Message": message
            }
            with open(Data_Validation_Report_Path, "w") as file:
                json.dump(report__file, file, indent=4)
            logging.info(f"Data validation report saved at {Data_Validation_Report_Path}")
            return True
        except Exception as e:
            logging.exception(f"Error during data validation: {e}")
            return False
        


#DataValidation().initiate_data_validation()