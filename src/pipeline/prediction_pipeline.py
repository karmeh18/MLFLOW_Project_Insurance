import sys
#from src.entity.config_entity import VehiclePredictorConfig
from src.constants import *
#from src.entity.s3_estimator import Proj1Estimator
from src.cloud_storage.aws_storage import AWS_Storage_Service
from src.logger import logging

from pandas import DataFrame
import joblib
import io


class VehicleData:
    def __init__(self,
                Gender,
                Age,
                Driving_License,
                Region_Code,
                Previously_Insured,
                Annual_Premium,
                Policy_Sales_Channel,
                Vintage,
                Vehicle_Age_lt_1_Year,
                Vehicle_Age_gt_2_Years,
                Vehicle_Damage_Yes
                ):
        """
        Vehicle Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age_lt_1_Year = Vehicle_Age_lt_1_Year
            self.Vehicle_Age_gt_2_Years = Vehicle_Age_gt_2_Years
            self.Vehicle_Damage_Yes = Vehicle_Damage_Yes

        except Exception as e:
            raise Exception(f"Error in VehicleData constructor: {e}", sys) from e

    def get_vehicle_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            return DataFrame(vehicle_input_dict)
        
        except Exception as e:
            raise Exception(f"Error in get_vehicle_input_data_frame method: {e}", sys) from e


    def get_vehicle_data_as_dict(self):
        """
        This function returns a dictionary from VehicleData class input
        """
        logging.info("Entered get_usvisa_data_as_dict method as VehicleData class")

        try:
            input_data = {
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
                "Vehicle_Age_lt_1_Year": [self.Vehicle_Age_lt_1_Year],
                "Vehicle_Age_gt_2_Years": [self.Vehicle_Age_gt_2_Years],
                "Vehicle_Damage_Yes": [self.Vehicle_Damage_Yes]
            }

            logging.info("Created vehicle data dict")
            logging.info("Exited get_vehicle_data_as_dict method as VehicleData class")
            return input_data

        except Exception as e:
            raise Exception(f"Error in get_vehicle_data_as_dict method: {e}", sys) from e

class VehicleDataClassifier:
    def predict(self, dataframe) -> str:
        """
        This is the method of VehicleDataClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of VehicleDataClassifier class")
            # Initialize AWS S3 client using your custom storage service
            s3 = AWS_Storage_Service(bucket_name=MODEL_BUCKET_NAME)
            # Get model bytes directly from S3 using the service's get_object method
            model_bytes = s3.get_object(AWS_Model_Save)
            # Load the model from bytes using joblib
            model = joblib.load(io.BytesIO(model_bytes))
            #Fetching Preprocessor from AWS
            preprocessor_bytes = s3.get_object(AWS_Preprocessor)
            # Load the preprocessor from bytes using joblib
            preprocessor = joblib.load(io.BytesIO(preprocessor_bytes))
            # Transform the input dataframe using the preprocessor
            dataframe = preprocessor.transform(dataframe)
            # Make prediction
            result = model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise Exception(f"Error in predict method of VehicleDataClassifier class: {e}", sys) from e