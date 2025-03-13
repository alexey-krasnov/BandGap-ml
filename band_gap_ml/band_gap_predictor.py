"""Band gap prefictor module."""
import argparse
import pandas as pd
import pickle

from band_gap_ml.vectorizer import FormulaVectorizer
from band_gap_ml.config import Config


def load_model(filepath):
    with open(filepath, 'rb') as file:
        return pickle.load(file)


def load_models_and_scalers(model_type, model_dir=None):
    """
    Load trained models and scalers for classification and regression.

    Parameters:
        model_type (str): Type of model to load (e.g., 'RandomForest', 'GradientBoosting', 'XGBoost')
        model_dir (Path or str, optional): Directory where models are stored. If None, uses default Config.MODELS_DIR

    Returns:
        tuple: (classifier_model, regressor_model, classification_scaler, regression_scaler)
    """
    model_paths = Config.get_model_paths(model_type, model_dir)
    classifier_model = load_model(model_paths['classification_model'])
    regressor_model = load_model(model_paths['regression_model'])
    scaler_class = load_model(model_paths['classification_scaler'])
    scaler_reg = load_model(model_paths['regression_scaler'])
    return classifier_model, regressor_model, scaler_class, scaler_reg


def prepare_features(input_data):
    """
    Prepare feature vectors for input chemical formulas using the FormulaVectorizer.

    Parameters:
        input_data (pd.DataFrame): Input data containing a 'Composition' column.

    Returns:
        pd.DataFrame: Transformed feature vectors.
    """
    vectorizer = FormulaVectorizer()
    features = []

    for formula in input_data['Composition']:
        vectorized = vectorizer.vectorize_formula(formula)
        features.append(vectorized)

    X = pd.DataFrame(features, columns=vectorizer.column_names)
    return X


def predict_band_gap(input_data, classifier_model, regressor_model, scaler_class, scaler_reg):
    """
    Predict band gaps using the provided classifier and regressor models.

    Parameters:
        input_data (pd.DataFrame): Feature vectors for chemical formulas.
        classifier_model: Trained classification model.
        regressor_model: Trained regression model.
        scaler_class: Fitted scaler for classification input data.
        scaler_reg: Fitted scaler for regression input data.

    Returns:
        list: Predicted band gaps (regression values or classification results).
    """
    X_scaled_class = scaler_class.transform(input_data)
    X_scaled_reg = scaler_reg.transform(input_data)

    classification_result = classifier_model.predict(X_scaled_class)
    regression_result = regressor_model.predict(X_scaled_reg)

    final_result = [
        regression_result[i] if classification_result[i] == 1 else classification_result[i]
        for i in range(len(classification_result))
    ]

    return final_result


def load_input_data(file_path):
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


def predict_eg_from_file(file_path=None, input_data=None, model_type='RandomForest', model_dir=None):
    """
    Predict band gaps from an input file containing chemical formulas.

    Parameters:
        file_path (str): Path to the input file. Default is None
        input_data (pd.DataFrame, optional): Input data with 'Composition' column. Defaults to None.
        model_type (str): Type of model to use for prediction. Default is 'RandomForest'.

    Returns:
        list: Predicted band gaps.
    """
    if file_path:
        input_data = load_input_data(file_path)

    if 'Composition' not in input_data.columns:
        first_column = input_data.columns[0]
        input_data.rename(columns={first_column: 'Composition'}, inplace=True)

    X = prepare_features(input_data)

    classifier_model, regressor_model, scaler_class, scaler_reg = load_models_and_scalers(model_type, model_dir)

    return predict_band_gap(X, classifier_model, regressor_model, scaler_class, scaler_reg)


def predict_eg_from_formula(formula, model_type='RandomForest', model_dir=None):
    """
    Predict band gap from a single chemical formula input.

    Parameters:
        formula (str or list): Chemical formula as a string or list of strings.
        model_type (str): Type of model to use for prediction. Default is 'RandomForest'.

    Returns:
        float or int: Predicted band gap value.
    """
    input_dict = {'Composition': []}
    if isinstance(formula, list):
        input_dict['Composition'].extend(formula)
    elif isinstance(formula, str):
        input_dict['Composition'].append(formula)
    input_data = pd.DataFrame(input_dict)

    X = prepare_features(input_data)

    classifier_model, regressor_model, scaler_class, scaler_reg = load_models_and_scalers(model_type, model_dir)

    return predict_band_gap(X, classifier_model, regressor_model, scaler_class, scaler_reg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Band Gap from Chemical Formula or File')
    parser.add_argument('--file', type=str, help='Path to input file (csv/excel) with chemical formulas')
    parser.add_argument('--formula', type=str, help='Single chemical formula for prediction')
    parser.add_argument('--model_type', type=str, default='RandomForest', help='Type of model to use for prediction: RandomForest, GradientBoosting, or XGBoost')
    parser.add_argument("--model_dir", type=str, default="models", help="Directory where models and scalers are stored")

    args = parser.parse_args()

    if args.file:
        predictions = predict_eg_from_file(args.file, model_type=args.model_typem, model_dir=args.model_dir)
        print("Predictions from file:", predictions)

    if args.formula:
        prediction = predict_eg_from_formula(args.formula, model_type=args.model_type, model_dir=args.model_dir)
        print(f"Prediction for formula '{args.formula}':", prediction)