import argparse
import datetime
import time
from pathlib import Path
from typing import List,  Union

import pandas as pd
import requests

from band_gap_ml.constants import API_URL


start = time.time()


class BandGapPredictorClient:
    """
    A client for interacting with the Band Gap Predictor API.

    Attributes:
        server_url (str): The URL of the Band Gap Predictor server.

    Methods:
        predict_band_gap(formula: Union[str, List[str]], model_type: str = "best_model") -> dict:
            Sends a POST request to the server with the chemical formula(s).
            Returns the prediction results in dictionary format.

        predict_from_file(file_path: str, model_type: str = "best_model") -> dict:
            Sends a POST request to the server with the path to a file containing chemical formulas.
            Returns the prediction results in dictionary format.

        healthcheck() -> dict:
            Sends a GET request to the server to check its health status.
            Returns the health status as a dictionary.
    """

    def __init__(self, server_url: str):
        """
        Initializes a BandGapPredictorClient instance.

        Parameters:
            server_url (str): The URL of the Band Gap Predictor server.
        """
        self.server_url = server_url

    def predict_band_gap(self, formula: Union[str, List[str]], model_type: str = "best_model"):
        """
        Sends a POST request to the server with the chemical formula(s).
        Returns the prediction results in dictionary format.

        Parameters:
            formula (str or List[str]): The chemical formula(s) to predict.
            model_type (str): The type of model to use for prediction.

        Returns:
            dict: Prediction results, including composition, is_semiconductor,
                  semiconductor_probability, and band_gap.
        """
        try:
            # Prepare the request data
            data = {
                "formula": formula,
                "model_type": model_type
            }

            # Send a POST request to the server
            response = requests.post(f'{self.server_url}/predict_bandgap_from_formula', json=data)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {'error': str(e)}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {'error': str(e)}

    def predict_from_file(self, file_path: str, model_type: str = "best_model"):
        """
        Sends a POST request to the server with the path to a file containing chemical formulas.
        Returns the prediction results in dictionary format.

        Parameters:
            file_path (str): The path to the file containing chemical formulas.
            model_type (str): The type of model to use for prediction.

        Returns:
            dict: Prediction results for all formulas in the file.
        """
        try:
            # Check if the path to the file is valid
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f'Invalid path provided: {file_path}')

            # Prepare the form data
            data = {
                "file_path": str(file_path_obj),
                "model_type": model_type
            }

            # Send a POST request to the server
            response = requests.post(f'{self.server_url}/predict_bandgap_from_file', data=data)
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {'error': str(e)}
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {'error': str(e)}

    def healthcheck(self):
        """
        Sends a GET request to the server to check its health status.
        Returns the health status as a dictionary.

        Returns:
            dict: The health status of the Band Gap Predictor server.
        """
        try:
            # Send a GET request to the server
            response = requests.get(f'{self.server_url}/healthcheck')
            response.raise_for_status()  # Raise an HTTPError for bad responses

            # Parse the JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            return {'error': str(e)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Client for Band Gap Predictor API")
    parser.add_argument("--formula", type=str, help="Chemical formula or comma-separated list of formulas")
    parser.add_argument("--file", type=str, help="Path to a file containing chemical formulas")
    parser.add_argument("--model_type", type=str, default="best_model",
                        help="Type of model to use (default: best_model)")
    parser.add_argument("--export_dir", type=str, default=".",
                        help="Export directory for the results")
    parser.add_argument("--server_url", type=str, default=API_URL,
                        help=f"URL of the Band Gap Predictor server (default: {API_URL})")
    args = parser.parse_args()

    # Create an instance of the client
    client = BandGapPredictorClient(args.server_url)

    # Check the health of the server
    health_status = client.healthcheck()
    print(f"Health Status: {health_status.get('status', 'Error')}")

    results = None

    # Process based on input type
    if args.formula:
        # Handle comma-separated list of formulas
        formulas = [f.strip() for f in args.formula.split(',')]
        if len(formulas) == 1:
            formulas = formulas[0]  # Single formula

        print(f"Predicting band gap for: {args.formula}")
        results = client.predict_band_gap(formulas, args.model_type)
    elif args.file:
        print(f"Predicting band gaps from file: {args.file}")
        results = client.predict_from_file(args.file, args.model_type)
    else:
        print("Error: Either --formula or --file must be provided.")
        parser.print_help()
        exit(1)

    if results and 'error' not in results:
        # Convert results to pandas DataFrame
        df = pd.DataFrame(results)
        print("\nPrediction Results:")
        print(df)

        # Save results to CSV
        timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        output_file = f'{args.export_dir}/band_gap_predictions_{timestamp}.csv'
        df.to_csv(output_file, index=False)
        print(f"\nResults saved to {output_file}")
    else:
        print(f"\nError: {results.get('error', 'Unknown error occurred')}")

    end = time.time()
    print(f"\nWork took {time.strftime('%H:%M:%S', time.gmtime(end - start))}")