# MLFLOW_Project_Insurance

Project: MLOps Insurance Data Pipeline
This project implements a robust, end-to-end MLOps pipeline for vehicle insurance prediction, integrating data engineering, model training, evaluation, and cloud deployment using AWS S3. The pipeline is designed for automation, reproducibility, and production-readiness, with modular components and CI/CD integration.

Key Features
Data Ingestion:
Connects to a MongoDB database, fetches insurance data, and exports it to local CSV files for further processing.

Data Validation:
Validates the ingested data against a defined schema, checks for missing columns, correct data types, and generates a validation report.

Data Transformation:
Applies preprocessing steps including scaling, encoding, and handling class imbalance (SMOTEENN), saving transformed datasets and preprocessing objects as artifacts.

Model Training:
Trains a Random Forest classifier on the processed data, evaluates model performance (accuracy, F1, precision, recall), and saves both the model and its metrics.

Model Evaluation & Conditional S3 Upload:
Compares the new model’s accuracy with the previous model stored in AWS S3. If the new model outperforms the old by a configurable threshold, the pipeline uploads the new data artifacts to S3.

AWS S3 Integration:
Handles S3 bucket creation, existence checks, and uploads of data/model artifacts. All S3 operations are robust and only performed when necessary.

Web Interface:
Includes a Flask-based web UI for model inference and triggering model training, with a modern, responsive design.

Testing & CI/CD:
Comprehensive pytest-based test suite for all pipeline components, with a GitHub Actions workflow for automated linting, testing, and formatting on every push or pull request.

Configuration & Logging:
Centralized configuration for paths, AWS, and MongoDB. Detailed logging for all pipeline steps and cloud operations.

Technologies Used
Python 3.11+
pandas, numpy, scikit-learn, imblearn
Flask (for web UI)
MongoDB (data source)
AWS S3 (artifact storage)
Pytest (testing)
GitHub Actions (CI/CD)
Docker-ready structure
Typical Workflow
Data is ingested from MongoDB and validated.
Data is transformed and preprocessed.
A model is trained and evaluated.
If the model is sufficiently improved, artifacts are uploaded to AWS S3.
All steps are logged and tested, with CI/CD ensuring code quality.
A web UI allows for easy predictions and retraining.