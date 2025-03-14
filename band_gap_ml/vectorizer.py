import numpy as np
import pandas as pd
from pymatgen.core.composition import Composition
from band_gap_ml.config import Config


class FormulaVectorizer:
    def __init__(self, elements_data_path=Config.ELEMENTS_PATH):
        self.elements_df = pd.read_csv(elements_data_path)
        self.elements_df.set_index('Symbol', inplace=True)
        self.column_names = [f'{stat}_{col}' for stat in ['avg', 'diff', 'max', 'min'] for col in
                             self.elements_df.columns]

    def vectorize_formula(self, formula):
        try:
            fractional_composition = Composition(formula).fractional_composition.as_dict()

            # Initialize arrays for avg, diff, max, min
            avg_feature = np.zeros(len(self.elements_df.iloc[0]))
            max_feature = np.zeros(len(self.elements_df.iloc[0]))
            min_feature = np.full(len(self.elements_df.iloc[0]), np.inf)  # Initialize with infinity for min
            element_list = []

            # Compute avg and gather elements for diff, max, and min
            for element, fraction in fractional_composition.items():
                avg_feature += self.elements_df.loc[element].values * fraction
                element_list.append(element)

            # Compute max, min, and diff based on elements in the formula
            max_feature = self.elements_df.loc[element_list].max().values
            min_feature = self.elements_df.loc[element_list].min().values
            diff_feature = max_feature - min_feature

            # Concatenate avg, diff, max, and min features
            features = np.concatenate([avg_feature, diff_feature, max_feature, min_feature])
            return features

        except Exception as e:
            print(f"Error processing formula {formula}: {e}")
            return [np.nan] * len(self.elements_df.columns) * 4  # Return appropriate length with NaNs
