"""
Configuration data for the package
"""
from typing import NamedTuple
from pathlib import Path

# Get the absolute path of the current file's directory
CURRENT_DIR = Path(__file__).resolve().parent

class ModelsNames(NamedTuple):
    """Class with model file names for classification and regression tasks."""
    classification_model: str
    scaler_classification_model: str
    regression_model: str
    scaler_regression_model: str

# Creating an instance of ModelsNames
models_names = ModelsNames(
    classification_model='classification_model.pkl',
    scaler_classification_model='scaler_class.pkl',
    regression_model='regression_model.pkl',
    scaler_regression_model='scaler_reg.pkl',
)

class Config:
    """
    Configuration class for managing paths and settings for the project.
    """
    # Paths for data and models directories
    MODELS_DIR = CURRENT_DIR / 'models'
    DATA_DIR = CURRENT_DIR / 'data'

    # Specific file paths
    ELEMENTS_PATH = DATA_DIR / 'elements.csv'
    CLASSIFICATION_DATA_PATH = DATA_DIR / 'train_classification.csv'
    REGRESSION_DATA_PATH = DATA_DIR / 'train_regression.csv'

    # Model paths
    CLASSIFICATION_MODEL_PATH = MODELS_DIR / models_names.classification_model
    SCALER_CLASSIFICATION_PATH = MODELS_DIR / models_names.scaler_classification_model
    REGRESSION_MODEL_PATH = MODELS_DIR / models_names.regression_model
    SCALER_REGRESSION_PATH = MODELS_DIR / models_names.scaler_regression_model
