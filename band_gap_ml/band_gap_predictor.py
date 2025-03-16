"""Band gap predictor module."""
import argparse
import pandas as pd
from typing import Optional, Union, List
from band_gap_ml.vectorizer import FormulaVectorizer
from band_gap_ml.config import Config


class BandGapPredictor:
    """
    A class for predicting band gaps of materials based on their chemical formulas.

    This class encapsulates the functionality to load models, prepare features,
    and predict band gaps using a combination of classification and regression models.
    """

    def __init__(self, model_type: str = 'best_model', model_dir: Optional[str] = None):
        """
        Initialize the BandGapPredictor with specified models.

        Parameters:
            model_type (str): Type of model to load (e.g., 'RandomForest', 'GradientBoosting', 'XGBoost').
                             Default is 'best_model' with RandomForest models.
            model_dir (str, optional): Directory where models are stored. If None, uses default Config.MODELS_DIR.
        """
        self.vectorizer = FormulaVectorizer()
        self.config = Config(model_type, model_dir)

    def prepare_features(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare feature vectors for input chemical formulas using the FormulaVectorizer.

        Parameters:
            input_data (pd.DataFrame): Input data containing a 'Composition' column.

        Returns:
            pd.DataFrame: Transformed feature vectors.
        """
        features = []

        for formula in input_data['Composition']:
            vectorized = self.vectorizer.vectorize_formula(formula)
            features.append(vectorized)

        X = pd.DataFrame(features, columns=self.vectorizer.column_names)
        return X

    def predict_band_gap(self, input_data: pd.DataFrame) -> List[float]:
        """
        Predict band gaps using the loaded classifier and regressor models.

        Parameters:
            input_data (pd.DataFrame): Feature vectors for chemical formulas.

        Returns:
            list: Predicted band gaps (regression values or classification results).
        """
        X_scaled_class = self.config.classification_scaler.transform(input_data)
        X_scaled_reg = self.config.regression_scaler.transform(input_data)

        classification_result = self.config.classification_model.predict(X_scaled_class)
        regression_result = self.config.regression_model.predict(X_scaled_reg)

        final_result = [
            regression_result[i] if classification_result[i] == 1 else classification_result[i]
            for i in range(len(classification_result))
        ]

        return final_result

    def predict_with_probabilities(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """
        Main method for predicting band gaps with classification probabilities.

        Parameters:
            input_data (pd.DataFrame): Feature vectors for chemical formulas.

        Returns:
            pd.DataFrame: DataFrame with predictions including class probabilities.
        """
        X_scaled_class = self.config.classification_scaler.transform(input_data)
        X_scaled_reg = self.config.regression_scaler.transform(input_data)

        # Get classification results and probabilities
        classification_result = self.config.classification_model.predict(X_scaled_class)
        class_probs = self.config.classification_model.predict_proba(X_scaled_class)

        # Get regression results
        regression_result = self.config.regression_model.predict(X_scaled_reg)

        # Create results DataFrame
        results = pd.DataFrame({
            'is_semiconductor': classification_result,
            'semiconductor_probability': class_probs[:, 1].round(4),
            'band_gap': regression_result.round(4),
        })

        return results

    @staticmethod
    def load_input_data(file_path: str) -> pd.DataFrame:
        """
        Load input data from a file (CSV or Excel).

        Parameters:
            file_path (str): Path to the input file.

        Returns:
            pd.DataFrame: Input data with 'Composition' column.
        """
        if file_path.endswith('.csv'):
            input_data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            input_data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

        return input_data

    def predict_from_file(self, file_path: Optional[str] = None, input_data: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """
        Predict band gaps from an input file containing chemical formulas.

        Parameters:
            file_path (str, optional): Path to the input file. Default is None.
            input_data (pd.DataFrame, optional): Input data with 'Composition' column. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame with predictions.
        """
        if file_path:
            input_data = self.load_input_data(file_path)

        if 'Composition' not in input_data.columns:
            first_column = input_data.columns[0]
            input_data.rename(columns={first_column: 'Composition'}, inplace=True)

        X = self.prepare_features(input_data)

        # Predict band gaps and probabilities
        predictions = self.predict_with_probabilities(X)

        # Combine original data with predictions
        result = pd.concat([input_data.reset_index(drop=True), predictions], axis=1)
        return result

    def predict_from_formula(self, formula: Union[str, List[str]]) -> pd.DataFrame:
        """
        Predict band gap from a single chemical formula or list of formulas.

        Parameters:
            formula (str or list): Chemical formula as a string or list of strings.

        Returns:
            pd.DataFrame: DataFrame with predictions.
        """
        input_dict = {'Composition': []}
        if isinstance(formula, list):
            input_dict['Composition'].extend(formula)
        elif isinstance(formula, str):
            input_dict['Composition'].append(formula)
        input_data = pd.DataFrame(input_dict)

        return self.predict_from_file(input_data=input_data)


def main():
    """Command line interface for band gap prediction."""
    parser = argparse.ArgumentParser(description='Predict Band Gap from Chemical Formula or File')
    parser.add_argument('--file', type=str, help='Path to input file (csv/excel) with chemical formulas')
    parser.add_argument('--formula', type=str, help='Single chemical formula for prediction')
    parser.add_argument('--model_type', type=str, default='best_model',
                        help='Type of model to use for prediction: RandomForest, GradientBoosting, or XGBoost')
    parser.add_argument("--model_dir", type=str, default=None,
                        help="Directory where models and scalers are stored")
    parser.add_argument("--output", type=str, default=None,
                        help="Path to save output predictions (CSV format)")

    args = parser.parse_args()

    predictor = BandGapPredictor(model_type=args.model_type, model_dir=args.model_dir)

    if args.file:
        predictions = predictor.predict_from_file(args.file)
        print(f"Predictions from file '{args.file}':")
        print(predictions)

        if args.output:
            predictions.to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")

    if args.formula:
        predictions = predictor.predict_from_formula(args.formula)
        print(f"Prediction for formula '{args.formula}':")
        print(predictions)

        if args.output:
            predictions.to_csv(args.output, index=False)
            print(f"Results saved to {args.output}")


if __name__ == '__main__':
    main()