"""Config module for managing paths and settings for the project.
"""
from pathlib import Path

# Get the absolute path of the current file's directory
CURRENT_DIR = Path(__file__).resolve().parent


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
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, 40],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'regression': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 20, 30, 40],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
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

    @classmethod
    def create_model_type_directory(cls, model_type, model_dir=None):
        """
        Create a directory for storing model files.

        Parameters:
            model_type (str): Type of model (e.g., 'RandomForest', 'GradientBoosting')
            model_dir (Path or str, optional): Base directory for models. If None, uses Config.MODELS_DIR

        Returns:
            Path: Path to the created directory
        """
        if not model_dir:
            model_dir = cls.MODELS_DIR / f"{model_type.lower()}"
        else:
            model_dir = Path(model_dir) / model_type.lower()

        # Create directory if it doesn't exist
        model_dir.mkdir(parents=True, exist_ok=True)
        print(f"Model directory created: {model_dir}")
        return model_dir

    @classmethod
    def get_model_paths(cls, model_type, model_dir=None):
        """
        Get paths for model and scaler files.

        Parameters:
            model_type (str): Type of model (e.g., 'RandomForest', 'GradientBoosting')
            model_dir (Path or str, optional): Base directory for models. If None, uses Config.MODELS_DIR

        Returns:
            dict: Dictionary with paths to model and scaler files
        """
        if not model_dir:
            model_dir = cls.MODELS_DIR / model_type.lower()
        else:
            model_dir = Path(model_dir) / model_type.lower()

        # Ensure the directory exists
        model_dir.mkdir(parents=True, exist_ok=True)

        return {
            'classification_model': model_dir / f'classification_model.pkl',
            'regression_model': model_dir / f'regression_model.pkl',
            'classification_scaler': model_dir / f'classification_scaler.pkl',
            'regression_scaler': model_dir / f'regression_scaler.pkl'
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

