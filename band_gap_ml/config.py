"""Config module for managing paths and settings for the project.
"""
from pathlib import Path
from typing import Optional
from functools import lru_cache
import pickle

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

    def __init__(self, model_type: str = 'best_model', model_dir: Optional[str] = None):
        """
        Initialize the Config instance with model settings.

        Parameters:
            model_type (str): Type of model to load (e.g., 'RandomForest', 'GradientBoosting', 'XGBoost').
                             Default is 'best_model' with RandomForest models.
            model_dir (str, optional): Directory where models are stored. If None, uses default Config.MODELS_DIR.
        """
        self.model_type = model_type
        self.model_dir = model_dir
        self._classification_model = None
        self._regression_model = None
        self._classification_scaler = None
        self._regression_scaler = None
        self._model_paths = self.get_model_paths(model_type, model_dir)

    @property
    def classification_model(self):
        """
        Returns the classification model, initializing it if necessary.

        Returns:
            object: The initialized classification model.
        """
        if self._classification_model is None:
            self._load_models()
        return self._classification_model

    @property
    def regression_model(self):
        """
        Returns the regression model, initializing it if necessary.

        Returns:
            object: The initialized regression model.
        """
        if self._regression_model is None:
            self._load_models()
        return self._regression_model

    @property
    def classification_scaler(self):
        """
        Returns the classification scaler, initializing it if necessary.

        Returns:
            object: The initialized classification scaler.
        """
        if self._classification_scaler is None:
            self._load_models()
        return self._classification_scaler

    @property
    def regression_scaler(self):
        """
        Returns the regression scaler, initializing it if necessary.

        Returns:
            object: The initialized regression scaler.
        """
        if self._regression_scaler is None:
            self._load_models()
        return self._regression_scaler

    @lru_cache(maxsize=None)
    def _load_models(self):
        """
        Load all models and scalers from pickle files.
        """
        self._classification_model = self._load_model(self._model_paths['classification_model'])
        self._regression_model = self._load_model(self._model_paths['regression_model'])
        self._classification_scaler = self._load_model(self._model_paths['classification_scaler'])
        self._regression_scaler = self._load_model(self._model_paths['regression_scaler'])

    @staticmethod
    def _load_model(filepath):
        """
        Load a model from a pickle file.

        Parameters:
            filepath (str or Path): Path to the pickle file.

        Returns:
            object: The loaded model.
        """
        with open(filepath, 'rb') as file:
            return pickle.load(file)

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
        Path(model_dir).mkdir(parents=True, exist_ok=True)
        print(f"Model directory created: {model_dir}")
        return model_dir

    @classmethod
    def get_model_paths(cls, model_type='best_model', model_dir: Optional[str] = None):
        """
        Get paths for model and scaler files.

        Parameters:
            model_type (str): Type of model to load (e.g., 'RandomForest', 'GradientBoosting', 'XGBoost').  Default is 'best_model' with RandomForest models.
            model_dir (str, optional): Directory where models are stored. If None, uses default Config.MODELS_DIR.

        Returns:
            dict: Dictionary with paths to model and scaler files
        """
        if not model_dir:
            model_dir = cls.MODELS_DIR / model_type.lower()
        else:
            print(f"Model directory: {model_dir}")
            model_dir = Path(model_dir) / model_type.lower()

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
