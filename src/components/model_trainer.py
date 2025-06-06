import pandas as pd
import numpy as np
import json
import os
import sys
from src.logger import logging
from src.utils.main_utils import *
from src.constants import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


#data=load_obj(r"D:\Vikash_dash_Demo_Spam_MLOps\MLFLOW_Project_Insurance\data\artifacts\preprocessor\preprocessed_test_data.pkl")
#print(data[-1])

class ModelTrainer:
    def __init__(self):
        self.train_data=load_obj(Preprocessed_Train_Data_Path)
        self.test_data=load_obj(Preprocessed_Test_Data_Path)

    def get_model_object_report(self):
        try:
            logging.info("Train Test Data Loaded")
            train=self.train_data
            test=self.test_data

            X_train,y_train,X_test,y_test=train[:,:-1],train[:,-1], test[:,:-1], test[:,-1]
            logging.info("Training Started with Random Forest with specific parameters")
            model = RandomForestClassifier(
                n_estimators=Model_Trainer_N_Estimator,
                min_samples_split=Model_Trainer_Min_Sample_Split,
                min_samples_leaf=Model_Trainer_Min_Sample_Leaf,
                max_depth=Min_Sample_Split_Max_Depth,
                criterion=Min_Sample_Split_Criterion,
                random_state=Min_Sample_Split_Random_State)
            
            logging.info("Model Training Started...")
            model.fit(X_train,y_train)
            logging.info("Model Training Done")

            y_pred=model.predict(X_test)
            accuracy=accuracy_score(y_test,y_pred)
            f1=f1_score(y_test,y_pred)
            precision=precision_score(y_test,y_pred)
            recall=recall_score(y_test,y_pred)

            metrics_report = {
                "Accuracy":accuracy,
                "F1_Score":f1,
                "Precision":precision,
                "recall":recall
            }
            os.makedirs(os.path.dirname(Model_Trainer_Artifact_Path),exist_ok=True)
            with open(Model_Trainer_Artifact_Path,"w") as file:
                json.dump(metrics_report,file,indent=4)
                logging.info(f"Model Metrics have been saved in {Model_Trainer_Artifact_Path}")
            save_obj(Model_Trainer_Dir_Path,model)
            return metrics_report, model
        except Exception as e:
            logging.exception(f"An Error occured during Random Forest {e}")

    def initiate_model_training(self):
        logging.info("Model Trainer Initiated")
        try:
            print("Starting Model Trainer Component")
            model_init,model=self.get_model_object_report()
            if model_init['Accuracy'] < Model_Trainer_Expected_Score:
                print(f"Model Accuracy is very less than {model_init['Accuracy']}")
            else:
                save_obj(Model_Trainer_Dir_Path,model)
        except Exception as e:
            logging.exception(f"An Eror occured during Initiating Model Training : {e}")


#ModelTrainer().initiate_model_training()

