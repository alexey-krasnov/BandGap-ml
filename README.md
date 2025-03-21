# BandGap-ml v0.4.0

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://github.com/alexey-krasnov/BandGap-ml/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/alexey-krasnov/BandGap-ml.svg)](https://github.com/alexey-krasnov/BandGap-ml/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/alexey-krasnov/BandGap-ml.svg)](https://github.com/alexey-krasnov/BandGap-ml/graphs/contributors)

## Table of Contents
- [Project Description](#project-description)
- [Prepare Workspace Environment with Conda](#prepare-python-workspace-environment-with-conda)
- [Models Construction](#models-construction)
- [Usage](#usage)
- [Author](#author)
- [License](#license)

## Project Description
Project for predicting band gaps of inorganic materials by using ML models.

## Try out new Frontend Web Interface running at: 
### https://bandgap-ml.streamlit.app/


## Prepare Python Workspace Environment with Conda
1. Download [Miniforge](https://github.com/conda-forge/miniforge) for Unix-like platforms (macOS & Linux)
```bash
# Download the installer using curl or wget or your favorite program:
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

# OR 
wget "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

# Run the script:
bash Miniforge3-$(uname)-$(uname -m).sh
```
and follow instructions. See the documentation for [Miniforge](https://github.com/conda-forge/miniforge) for more information.


```bash
# 2. Create and activate the conda environment
conda create --name bandgap-ml "python<3.13"
conda activate bandgap-ml

# 3. Install BandGap-ml
# 3.1 From PyPI
pip install BandGap-ml

# 3.2 Or install the latest version from the GitHub repository
pip install git+https://github.com/alexey-krasnov/BandGap-ml.git

# 3.3 Or install the latest version in editable mode from the GitHub repository
git clone https://github.com/alexey-krasnov/BandGap-ml.git
cd BandGap-ml
pip install -e .
```
- Where -e means "editable" mode.

## Data source
For training Random Forest Classifier and Regression models, we adopted data provided in the following paper:
- Zhuo. Y, Mansouri Tehrani., and Brgoch. J, Predicting the band gaps of inorganic solids by machine learning, J. Phys. Chem. Lett. 2018, 9, 1668-1673.

## Models construction
To perform model training, validation, and testing, as well as saving your trained model, run the following command in the CLI:
```bash
python band_gap_ml/model_training.py
```
This command executes the training and evaluation of RandomForestClassifier and RandomForestRegressor models using the predefined paths in the module.

## Usage
We provide several options to use the BandGap-ml package.

### 1. Jupyter Notebook
A [Jupyter Notebook file](notebooks/band_gap_prediction_workflow.ipynb) in the `notebooks` directory provides an easy-to-use interface for training models and using them for Band Gap predictions.

### 2. Python Code
You can use the package directly in your Python code:

#### 2.1 Train models
```python
from band_gap_ml.model_training import train_and_save_models

train_and_save_models()
```
#### 2.2 Make predictions of band gaps by using the BandGapPredictor class:
```python
from band_gap_ml.band_gap_predictor import BandGapPredictor

# Initialize the predictor with default best model
predictor = BandGapPredictor()

# Or specify a different model type and path to the model
# predictor = BandGapPredictor(model_type='RandomForest', model_dir= <YOUR_PATH_TO_THE_MODEL>)
# predictor = BandGapPredictor(model_type='GradientBoosting')
# predictor = BandGapPredictor(model_type='XGBoost')

# Prediction from csv file containing chemical formulas
input_file = 'samples/to_predict.csv'
predictions_df = predictor.predict_from_file(input_file)
print(predictions_df)

# Prediction from one or multiple chemical formulas
formula_1 = 'BaLa2In2O7'
formula_2 = 'TiO2'
formula_3 = 'Bi4Ti3O12'

# Single formula prediction
single_prediction = predictor.predict_from_formula(formula_1)
print(single_prediction)

# Multiple formulas prediction
multiple_predictions = predictor.predict_from_formula([formula_1, formula_2, formula_3])
print(multiple_predictions)

# Save predictions to a CSV file
multiple_predictions.to_csv('predictions_results.csv', index=False)
```

### 3. Web Service
You can use BandGap-ml as a web service in two ways:

#### 3.1 Use our hosted web interface at: **https://bandgap-ml.streamlit.app/**

#### 3.2  Run the web service locally:
- Prerequisites
  - [Docker](https://docs.docker.com/get-docker/)
  - [Docker Compose](https://docs.docker.com/compose/install/)
  - [Git](https://git-scm.com/downloads)
- Build and start the Docker containers
```bash
docker compose up -d --build
```

- Once the containers are running, you can access:
  -  BandGap-ml frontend web interface in your browser at http://localhost:8080
  - Backend API: http://localhost:3000
  - API Documentation: http://localhost:3000/docs


- The application runs two main containers:
  - `frontend`: Vue.js application (Port 8080)
  - `backend`: FastAPI application running with uvicorn (Port 3000)

- To stop the containers:

```bash
docker compose down
```

- To check container status:

```bash
docker compose ps
```

- To view container logs:

```bash
# All containers
docker compose logs

# Specific container
docker compose logs frontend
docker compose logs backend
```

## Author
Dr. Aleksei Krasnov
alexeykrasnov1989@gmail.com

## Citation
- Zhuo. Y, Mansouri Tehrani., and Brgoch. J, Predicting the band gaps of inorganic solids by machine learning, J. Phys. Chem. Lett. 2018, 9, 1668-1673. https://doi.org/10.1021/acs.jpclett.8b00124

## License
This project is licensed under the MIT - see the [LICENSE.md](LICENSE.md) file for details.