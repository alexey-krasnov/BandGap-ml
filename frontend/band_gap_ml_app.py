import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import psutil
import subprocess
from streamlit_navigation_bar import st_navbar
from about import show_about
from docs import show_docs
from band_gap_ml.constants import API_URL


def is_uvicorn_running():
    """
    Checks if there's any running process with 'uvicorn' and 'band_gap_ml.app:app'.
    Returns True if such a process is found, otherwise False.
    """
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and "uvicorn" in cmdline and "band_gap_ml.app:app" in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def start_uvicorn():
    log_file = open("band_gap_ml_uvicorn_log.txt", "w")
    process = subprocess.Popen(
        ["uvicorn", "band_gap_ml.app:app", "--host", "127.0.0.1", "--port", "5039", "--workers", "1", "--timeout-keep-alive", "3600"],
        stdout=log_file,
        stderr=subprocess.STDOUT
    )
    return process


def check_api_connection():
    try:
        response = requests.get(f"{st.session_state.api_url}/healthcheck")
        if response.status_code == 200:
            return True, response.json().get('status', 'Connected')
        return False, f"Error: Status code {response.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

# Function to handle file download
def download_predictions_as_csv(data_frame, prefix="predicted_band_gaps"):
    """
    Function to create a downloadable CSV file with predictions and timestamp in the filename.

    Parameters:
        data_frame (pd.DataFrame): The data frame containing the predictions.
        prefix (str): Prefix for the file name.
    """
    # Get the current timestamp for the filename
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    file_name = f"{prefix}_{timestamp}.csv"

    # Convert DataFrame to CSV and create a download button
    csv = data_frame.to_csv(index=False)
    st.download_button(
        label="Download Predictions as CSV",
        data=csv,
        file_name=file_name,
        mime="text/csv"
    )


def predict_from_api_formulas(formulas, model_type):
    """
    Send formulas to the API for prediction.

    Parameters:
        formulas (list): List of chemical formulas
        model_type (str): Type of model to use for prediction

    Returns:
        pd.DataFrame: DataFrame with predictions or None if error
    """
    try:
        # Prepare the request data
        data = {
            "formula": formulas,
            "model_type": model_type
        }

        # Send request to API
        response = requests.post(
            f"{st.session_state.api_url}/predict_bandgap_from_formula",
            json=data
        )

        if response.status_code == 200:
            # Convert response to DataFrame
            predictions = response.json()
            df = pd.DataFrame(predictions)
            # Rename columns to match the expected format
            df = df.rename(columns={
                'composition': 'Composition',
                'is_semiconductor': 'is_semiconductor',
                'semiconductor_probability': 'semiconductor_probability',
                'band_gap': 'band_gap'
            })
            return df
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def show_footer():
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f2f2f2;
            color: black;
            text-align: center;
            padding: 5px;
            z-index: 999;
            font-size: 12px;
        }
        .footer a {
            color: #1f77b4;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        </style>
        <div class="footer">
            <p>&copy; 2024 BandGap-ml. Predicting material band gaps based on chemical composition. <br>
            Developed by <a href="https://github.com/alexey-krasnov" target="_blank">Aleksei Krasnov</a>. All rights reserved.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )



def show_home():
    # Set title and description
    st.title('BandGap-ml: Band Gap Prediction')
    st.write("""
        This app allows you to predict the band gap of materials either by uploading a CSV file or by entering chemical formulas.
    """)

    # API connection settings
    if 'api_url' not in st.session_state:
        st.session_state.api_url = API_URL

    # Add options in the sidebar
    st.sidebar.header("Options")

    # Model selection using selectbox in sidebar
    selected_model = st.sidebar.selectbox(
        "Select Model for Prediction",
        ["best_model", "RandomForest", "GradientBoosting", "XGBoost"],
        index=0,
        format_func=lambda x: "Best Model" if x == "best_model" else x
    )

    # Update session state with selected model
    st.session_state.selected_model = selected_model

    # Display model information based on selection
    st.sidebar.subheader("Model Information")
    if st.session_state.selected_model == 'best_model':
        st.sidebar.write("""
        The best model is a RandomForest-based model that has been optimized for band gap prediction.
        """)
    elif st.session_state.selected_model == 'RandomForest':
        st.sidebar.write("""
        Random Forest is an ensemble learning method that operates by constructing multiple decision trees during training.
        """)
    elif st.session_state.selected_model == 'GradientBoosting':
        st.sidebar.write("""
        Gradient Boosting is a machine learning technique that builds an ensemble of decision trees in a stage-wise fashion.
        """)
    elif st.session_state.selected_model == 'XGBoost':
        st.sidebar.write("""
        XGBoost is an optimized distributed gradient boosting library designed to be highly efficient, flexible and portable.
        """)

    # Add a button to check API health
    if st.sidebar.button("Check API Health"):
        api_status, status_message = check_api_connection()
        if api_status:
            st.sidebar.success(f"API Status: {status_message}")
        else:
            st.sidebar.error(f"API Status: {status_message}")

    # Section to train models (optional for users who want to retrain)
    train_button = st.button('Train Models')
    if train_button:
        st.warning("Model training is handled by the backend service. Please contact the administrator to retrain models.")

    # Display currently selected model in the main area
    st.info(f"Currently using: **{selected_model if selected_model != 'best_model' else 'Best Model'}**")

    # File upload for CSV
    uploaded_file = st.file_uploader("Upload CSV file with chemical formulas written in the first column. ", type=["csv"])
    if uploaded_file:
        try:
            input_data = pd.read_csv(uploaded_file)

            # Predict band gaps from the uploaded file
            if st.button('Predict Band Gaps from File'):
                with st.spinner('Predicting band gaps...'):
                    # Extract formulas from the first column
                    if 'Composition' in input_data.columns:
                        formulas = input_data['Composition'].tolist()
                    else:
                        # Use the first column if 'Composition' doesn't exist
                        first_col = input_data.columns[0]
                        formulas = input_data[first_col].tolist()

                    # Use the API for prediction
                    predictions = predict_from_api_formulas(formulas, st.session_state.selected_model)
                    if predictions is not None:
                        st.write("Predictions from the uploaded file:")
                        st.write(predictions)
                        # Call the function to allow file download
                        download_predictions_as_csv(predictions)
        except Exception as e:
            st.error(f"Error reading the file: {e}")

    # Section for entering chemical formulas
    st.subheader("Or, enter chemical formulas manually:")
    formulas_input = st.text_area(
        "Enter one or more chemical formulas (separate by commas):",
        "BaLa2In2O7, TiO2, Bi4Ti3O12"
    )

    if formulas_input:
        formulas = [formula.strip() for formula in formulas_input.split(",")]
        if st.button('Predict Band Gaps from Formulas'):
            with st.spinner('Predicting band gaps...'):
                # Use the API for prediction
                predictions = predict_from_api_formulas(formulas, st.session_state.selected_model)
                if predictions is not None:
                    st.write("Predictions for the entered formulas:")
                    st.write(predictions)
                    # Call the function to allow file download
                    download_predictions_as_csv(predictions, prefix="predicted_band_gaps_formulas")


# This implementation is causing error when hide Slide Bar. Then it cannot be unhidden and then displayed again.
def main():
    st.set_page_config(
        page_title="ChemICR: Chemical Image Classification and Recognition",
        page_icon=":test_tube:",
        layout="wide"
    )

    pages = ["Home",
             "About",
             "API Documentation",
             "GitHub",
             ]
    urls = {"GitHub": "https://github.com/ontochem/ChemIC"}

    styles = {
        "nav": {"background-color": "#333333", "justify-content": "middle", "font-family": "Bahnschrift, sans-serif", "padding": "0 10px"},
        "img": {"padding-right": "2px", "background-color": "#FFFFFF", "border-radius": "4px"},
        "span": {"color": "#FFFFFF", "padding": "10px", "font-family": "Bahnschrift, sans-serif", "background-color": "#555555", "margin": "0 5px", "border-radius": "3px"},
        "active": {"color": "#FFFFFF", "background-color": "#777777", "font-weight": "bold", "padding": "10px", "font-family": "Bahnschrift, sans-serif", "border-radius": "3px"},
        "hover": {"background-color": "#444444", "color": "#FFFFFF"}
    }

    options = {"show_menu": False, "show_sidebar": False}

    page = st_navbar(pages,
                     urls=urls,
                     styles=styles,
                     options=options,
                     )

    # Display content based on the selected page
    if page == "Home":
        show_home()
    elif page == "About":
        show_about()
    elif page == "API Documentation":
        show_docs()
    elif page == "GitHub":
        st.markdown("[Visit GitHub Repository](https://github.com/alexey-krasnov/BandGap-ml)")
    else:
        show_home()  # Default to home page if no valid selection

    show_footer()

if __name__ == "__main__":
    try:
        if not is_uvicorn_running():
            backend_process = start_uvicorn()
        else:
            print("Uvicorn is already running.")
    except Exception as e:
        print(f"Error starting backend server: {e}")
    else:
        main()