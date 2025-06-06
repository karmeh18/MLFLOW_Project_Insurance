import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer

from src.constants import *
from src.logger import logging
from src.utils.main_utils import read_yaml, save_obj

class DataTransformation:
    def __init__(self):
        try:
            self.schema = read_yaml(Schema_Yaml_File_Path)
            self.train_data = pd.read_csv(Training_Data_Path)
            self.test_data = pd.read_csv(Testing_Data_Path)
        except Exception as e:
            logging.exception(f"Error initializing DataTransformation: {e}")
            raise e
        
    def get_data_transformation_pipeline(self) -> Pipeline:
        """
        Create a data transformation pipeline.
        :return: A scikit-learn Pipeline object for data transformation.
        """
        logging.info("Transformer Initialized: StandardScaler-MinMaxScaler")
        try:
            numeric_transformer=StandardScaler()
            min_max_scaler=MinMaxScaler()
            
            num_features = self.schema['numerical_columns']
            mm_columns = self.schema['mm_columns']
            logging.info("Cols loaded from schema file")

            preprocessor =  ColumnTransformer(
                transformers = [
                    ('num', numeric_transformer, num_features),
                    ('min_max', min_max_scaler, mm_columns)
                ],
                remainder='passthrough'
            )

            final_pipeline = Pipeline(steps = [("Preprocessor",preprocessor)])
            logging.info("Final Pipeline created successfully")
            return final_pipeline
        except Exception as e:
            logging.exception(f"Error creating data transformation pipeline: {e}")
            raise e
        
    def map_gender_column(self,df: pd.DataFrame) -> pd.DataFrame:
        """
        Map Gender column to 1 and 0
        """
        try:
            logging.info("Mapping of Gender column started")
            df["Gender"] = df["Gender"].map({'Female':0, 'Male':1}).astype(int)
            logging.info("Mapping of Gender column completed.")
            return df
        except Exception as e:
            logging.exception(f"Error Raised while mapping: {e}")
            raise e
    
    def create_dummy_variable(self,df):
        logging.info("Creating dummy variables for categorical columns")
        df=pd.get_dummies(df, columns=self.schema['categorical_columns'], drop_first=True)
        logging.info("Dummy variables created successfully")
        return df
    
    def rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Rename columns based on the schema.
        :param df: DataFrame to rename columns.
        :return: DataFrame with renamed columns.
        """
        logging.info("Renaming columns based on schema")
        df = df.rename(columns = 
            {"Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
            "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
        })
        for col in ["Vehicle_Age_lt_1_Year", "Vehicle_Age_gt_2_Years", "Vehicle_Damage_Yes"]:
            if col in df.columns:
                df[col] = df[col].astype('int')
        return df

    def initiate_data_transformation(self) -> None:
        """
        Initiate the data transformation process.
        :return: None
        """
        try:
            logging.info("Starting data transformation operations")
            #input_train_data = self.train_data.drop(columns=[self.schema["target_column"]])
            #input_test_data = self.test_data.drop(columns=[self.schema["target_column"]])
            input_train_data = self.train_data
            input_test_data = self.test_data
            logging.info("Dropped target column from train and test data")
            y_train = self.train_data[self.schema["target_column"]]
            y_test = self.test_data[self.schema["target_column"]]
            logging.info("Separated target column from train and test data")

            #apply transformations
            input_train_data = self.map_gender_column(input_train_data)
            input_train_data = self.create_dummy_variable(input_train_data)
            input_train_data = self.rename_columns(input_train_data)

            input_test_data = self.map_gender_column(input_test_data)
            input_test_data = self.create_dummy_variable(input_test_data)
            input_test_data = self.rename_columns(input_test_data)
            logging.info("Completed Custom transformations to train and test data")

            preprocessor = self.get_data_transformation_pipeline()
            input_feature_arr_train = preprocessor.fit_transform(input_train_data)
            input__feature_arr_test = preprocessor.transform(input_test_data)
            logging.info("Applied preprocessing to train data")

            logging.info("Applying SMOTEENN for handling class imbalance")
            smote_enn = SMOTEENN(random_state=Random_State)
            input_feature_train_final, taregt_feature_train_final = smote_enn.fit_resample(input_feature_arr_train, y_train)
            input_feature_test_final, target_feature_test_final = smote_enn.fit_resample(input__feature_arr_test, y_test)
            logging.info("SMOTEENN applied successfully to both train and test data")

            train_arr = np.c_[input_feature_train_final, taregt_feature_train_final]
            test_arr = np.c_[input_feature_test_final, target_feature_test_final]
            logging.info("Combined input and target features for train and test data")

            logging.info("Saving transformed data to artifacts")
            os.makedirs(os.path.dirname(Preprocessor_Obj_Path), exist_ok=True)
            save_obj(Preprocessor_Obj_Path, preprocessor)

            logging.info("Saving preprocessed train and test data")
            save_obj(Preprocessed_Train_Data_Path, train_arr)
            save_obj(Preprocessed_Test_Data_Path, test_arr)

            logging.info("Data Transformation completed successfully")
        except Exception as e:
            logging.exception(f"Error in data transformation pipeline: {e}")
            raise e


#DataTransformation().initiate_data_transformation()






