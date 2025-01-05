# BandGap-ml v1.0

[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://GitHub.com/BandGap-ml/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/alexey-krasnov/Band_Gap_ML.svg)](https://github.com/alexey-krasnov/Band_Gap_ML/issues)
[![GitHub contributors](https://img.shields.io/github/contributors/alexey-krasnov/Band_Gap_ML.svg)](https://github.com/alexey-krasnov/Band_Gap_ML/graphs/contributors)


## Table of Contents
- [Project Description](#project-description)
- [Prepare Workspace Environment with Conda](#prepare-workspace-environment-with-conda)
- [Model Construction](#model-construction)
- [Models Download](#models-download)
- [Jupyter Notebook](#jupyter-notebook)
- [Author](#author)
- [Citation](#citation)
- [References](#references)
- [License](#license)

## Project Description
Project for predicting band gaps of inorganic materials by using ML models

## Prepare Python Workspace Environment with Conda
```bash
# 1. Create and activate the conda environment
conda create --name bandgap-ml "python<3.12"
conda activate bandgap-ml

# 2. Install BandGap-ml
# 2.1 From PyPI
TODO: upload

# 2.2 Or, install from the GitHub repository
pip install git+https://github.com/alexey-krasnov/Band_Gap_ML.git

# 2.3 Or, install in editable mode from the GitHub repository
git clone https://github.com/alexey-krasnov/Band_Gap_ML.git
cd Band_Gap_ML
pip install -r requirements.txt
pip install -e .
```
- Where -e means "editable" mode.
 
## Model construction
To perform model training, validation, and testing, as well as saving your trained model, run the following command in the CLI:
```bash
python band_gap_ml/model_training.py
```
This command executes the training and evaluation of RandomForestClassifier and RandomForestRegressor models using the predefined paths in the module.

## Models download
If the models have not been downloaded yet, download them from Zenodo as an archive: [XXX](XXX). 
Unzip it into the [band_gap_ml/models](band_gap_ml/models) directory. The models directory should contain the pre-trained models for band gap prediction.

## Usage
You can try out the user frontend web interface at TODO

## Jupyter Notebook
The [band_gap_workflow.ipynb](notebooks/band_gap_workflow.ipynb) notebook in the `notebooks` directory provides an easy-to-use interface for training models and use them for Band Gap predictions.

## Author
Dr. Aleksei Krasnov
alexeykrasnov1989@gmail.com

## Citation

## References

## License
This project is licensed under the MIT - see the [LICENSE.md](LICENSE.md) file for details.