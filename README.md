# BandGap-ml v1.1

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://github.com/alexey-krasnov/BandGap-ml/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/alexey-krasnov/BandGap-ml.svg)](https://github.com/alexey-krasnov/BandGap-ml/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/alexey-krasnov/BandGap-ml.svg)](https://github.com/alexey-krasnov/BandGap-ml/graphs/contributors)

## Table of Contents
- [Project Description](#project-description)
- [Prepare Workspace Environment with Conda](#prepare-workspace-environment-with-conda)
- [Models Construction](#models-construction)
- [Usage](#usage)
- [Author](#author)
- [License](#license)

## Project Description
Project for predicting band gaps of inorganic materials by using ML models.

## Try out new Frontend Web Interface running at:https://bandgap-ml.streamlit.app/


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
Zhuo. Y, Mansouri Tehrani., and Brgoch. J, Predicting the band gaps of inorganic solids by machine learning, J. Phys. Chem. Lett. 2018, 9, 1668-1673.

## Models construction
To perform model training, validation, and testing, as well as saving your trained model, run the following command in the CLI:
```bash
python band_gap_ml/model_training.py
```
This command executes the training and evaluation of RandomForestClassifier and RandomForestRegressor models using the predefined paths in the module.

## Usage
We provide several options to use the package

### 1. Jupyter Notebook file:
[Jupyter Notebook file](notebooks/band_gap_prediction_workflow.ipynb) in the `notebooks` directory provides an easy-to-use interface for training models and use them for Band Gap predictions.

### 2. Use package inside your Python Code:
Train models
```python
from band_gap_ml.model_training import train_and_save_models

train_and_save_models()
```
Use models to make predictions of Band Gaps
```python
from band_gap_ml.band_gap_predictor import predict_eg_from_file, predict_eg_from_formula    

# Prediction from csv file containing chemical formulas
input_file = '../samples/to_predict.csv'
predictions = predict_eg_from_file(input_file)
print(predictions)

#  Prediction from one or multiple chemical formula
formula_1 = 'BaLa2In2O7'
formula_2 = 'TiO2'
formula_3 = 'Bi4Ti3O12'

predictions = predict_eg_from_formula(formula=[formula_1, formula_2, formula_3])
print(predictions)
```

### 3. Use frontend web interface
- Go to https://bandgap-ml.streamlit.app/ to check out the web interface
- Or run web interface on your local machine. In CLI run the command:
```bash
streamlit run frontend/band_gap_ml_app.py --server.address=0.0.0.0 --server.port=5005
```
The command will refer you to the BandGap-ml user web interface.

## Author
Dr. Aleksei Krasnov
alexeykrasnov1989@gmail.com

## Citation
- Zhuo. Y, Mansouri Tehrani., and Brgoch. J, Predicting the band gaps of inorganic solids by machine learning, J. Phys. Chem. Lett. 2018, 9, 1668-1673. https://doi.org/10.1021/acs.jpclett.8b00124

## License
This project is licensed under the MIT - see the [LICENSE.md](LICENSE.md) file for details.