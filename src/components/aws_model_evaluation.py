import json
from src.logger import logging
from src.cloud_storage.aws_storage import AWS_Storage_Service
from src.constants import *
from src.components.aws_model_pusher import S3ModelUploader

#aws_service = AWS_Storage_Service(MODEL_BUCKET_NAME)

class AWS_Model_Evaluation:
    def __init__(self):
        self.MODEL_KEY = AWS_Model_Save
        self.METADATA_KEY = AWS_Model_Artifact

    def get_accuracy_from_s3(key=AWS_Model_Artifact):
        aws_service = AWS_Storage_Service(MODEL_BUCKET_NAME)
        response = aws_service.s3_client.get_object(Bucket=MODEL_BUCKET_NAME, Key=AWS_Model_Artifact)
        content = json.loads(response['Body'].read().decode('utf-8'))
        accuracy = content.get('accuracy', content.get('Accuracy'))
        return accuracy

    def main(new_accuracy, local_model_path=None):
        model_pusher = S3ModelUploader()
        # Check if model and metadata exist in S3
        if model_pusher.model_exists():
            old_accuracy = get_accuracy_from_s3()
            print(f"Existing model accuracy: {old_accuracy}")
            print(f"New model accuracy: {new_accuracy}")
            if new_accuracy > old_accuracy + AWS_MODEL_EVALUATION_THRESHOLD:
                print("New model accuracy is sufficiently better. Uploading new model and metadata...")
                model_pusher.upload_model(Model_Trainer_Dir_Path, AWS_Model_Save)
            else:
                print("New model accuracy is not better enough. Skipping upload.")
        else:
            print("No existing model found. Uploading new model and metadata...")
            model_pusher.upload_model(Model_Trainer_Dir_Path, AWS_Model_Save)

AWS_Model_Evaluation.main(1.0, local_model_path=Model_Trainer_Dir_Path)
