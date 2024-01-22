import pandas as pd
import polars as pl
from IPython.display import display

data = pd.read_csv('../example/Tree_Data.csv')


class TreeDataCleaner:
    def __init__(self, data):
        self.data = data

    def cleaned_data(self):
        # Handle missing values in the 'EMF' column by filling with the mean
        self.data['EMF'].fillna(self.data['EMF'].mean(), inplace=True)

        # Check for any null values in the dataset
        null_values_check = self.data.isnull().any()

        # Print columns with null values, if any
        if null_values_check.any():
            print("Columns with null values:")
            print(null_values_check[null_values_check].index.tolist())

        # Remove duplicate rows in the dataset
        self.data = self.data.drop_duplicates()

        # Display the cleaned dataset
        display(self.data)

# Example usage:
tree_cleaner = TreeDataCleaner(data)


# Process and view datasets for each function
raw_cleaned = tree_cleaner.cleaned_data()
