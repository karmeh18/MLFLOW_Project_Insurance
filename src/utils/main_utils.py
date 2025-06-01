import os
import yaml
import pickle
import sys

def read_yaml(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
        
    Returns:
        dict: Content of the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
      raise Exception(f"Error reading YAML file {file_path}: {e}")  
def save_obj(file_path: str, obj: object) -> None:
    """
    Saves an object to a file using dill.
    
    Args:
        file_path (str): Path to the file where the object will be saved.
        obj (object): The object to save.
    """
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise Exception(f"Error saving object to {file_path}: {e}")