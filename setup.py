from setuptools import setup, find_packages

def read_requirements():
    """Read the requirements.txt file and return a list of dependencies."""
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BandGap-ml",
    version="1.1",
    description="Project for predicting band gaps of inorganic materials by using ML models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dr.Aleksei Krasnov",
    author_email="alexeykrasnov1989@gmail.com",
    license="MIT",
    python_requires=">=3.10,<3.13",
    classifiers=[
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],

    url="https://github.com/alexey-krasnov/Band_Gap_ML",
    packages=find_packages(exclude=["tests", "tests.*", "Benchmark"]) + [
        'band_gap_ml.data',
        'band_gap_ml.models'
    ],
    include_package_data=True,  # Ensure package data is included
    package_data={
        'band_gap_ml': [
            'data/*.csv',  # Include all CSV files in the data subfolder
            'models/*.pkl',  # Include all model files in the models subfolder
        ],
    },
    install_requires=read_requirements(),
)
