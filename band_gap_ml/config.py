"""Config module for managing paths and settings for the project.
"""
from typing import NamedTuple
from pathlib import Path

# Get the absolute path of the current file's directory
CURRENT_DIR = Path(__file__).resolve().parent


class ModelsNames(NamedTuple):
    """Class with model file names for classification and regression tasks."""
    model: str
    scaler: str


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

    # Model types
    MODEL_TYPES = {
        'RandomForest': {
            'classification': 'sklearn.ensemble.RandomForestClassifier',
            'regression': 'sklearn.ensemble.RandomForestRegressor'
        },
        'GradientBoosting': {
            'classification': 'sklearn.ensemble.GradientBoostingClassifier',
            'regression': 'sklearn.ensemble.GradientBoostingRegressor'
        },
        'XGBoost': {
            'classification': 'xgboost.XGBClassifier',
            'regression': 'xgboost.XGBRegressor'
        }
    }

    # Default grid search parameters
    DEFAULT_GRID_PARAMS = {
        'RandomForest': {
            'classification': {
                'n_estimators': [100, 200, 300, 400],
                'max_depth': [None, 10, 20, 30, 40],
                'min_samples_split': [2, 5, 10, 15],
                'min_samples_leaf': [1, 2, 4, 6]
            },
            'regression': {
                'n_estimators': [100, 200, 300, 400],
                'max_depth': [None, 10, 20, 30, 40],
                'min_samples_split': [2, 5, 10, 15],
                'min_samples_leaf': [1, 2, 4, 6]
            }
        },
        'GradientBoosting': {
            'classification': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 4, 5],
                'min_samples_split': [2, 5, 10]
            },
            'regression': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 4, 5],
                'min_samples_split': [2, 5, 10]
            }
        },
        'XGBoost': {
            'classification': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 4, 5],
                'min_child_weight': [1, 3, 5]
            },
            'regression': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 4, 5],
                'min_child_weight': [1, 3, 5]
            }
        }
    }

    @staticmethod
    def get_model_paths(model_type):
        models_names = ModelsNames(
            model=f'{model_type.lower()}.pkl',
            scaler=f'{model_type.lower()}_scaler.pkl'
        )
        model_dir = Config.MODELS_DIR / model_type.lower()
        return {
            'classification_model': model_dir / f'classification_{models_names.model}',
            'regression_model': model_dir / f'regression_{models_names.model}',
            'classification_scaler': model_dir / f'classification_{models_names.scaler}',
            'regression_scaler': model_dir / f'regression_{models_names.scaler}'
        }

    @staticmethod
    def get_default_grid_params(model_type, task):
        """
        Get the default grid search parameters for a given model type and task.

        :param model_type: str, the type of model (e.g., 'RandomForest', 'GradientBoosting', 'XGBoost')
        :param task: str, either 'classification' or 'regression'
        :return: dict, default grid search parameters
        """
        return Config.DEFAULT_GRID_PARAMS.get(model_type, {}).get(task, {})

