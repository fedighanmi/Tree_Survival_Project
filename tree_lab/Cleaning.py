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

    def process_species_data(self):
        df_subset = self.data[['Species', 'Alive', 'Event']]
        df_subset['Alive'] = df_subset['Alive'].replace('X', 1)
        df_subset['Alive'] = df_subset['Alive'].fillna(0)
        df_subset = df_subset.rename(columns={'Event': 'Dead'})

        by_species_df = df_subset.groupby('Species').sum()

        # Create and add a new column containing the species names
        new_column_data = ["Acer saccharum", "Prunus serotina", "Quercus alba", "Quercus rubra"]
        by_species_df.insert(0, 'Species', new_column_data)

        species_df = pl.DataFrame(by_species_df)

        # Convert Polars DataFrame to Pandas DataFrame
        species_pandas_df = species_df.to_pandas()

        data_counts = species_pandas_df.melt(id_vars="Species",
                                             value_vars=["Alive"],
                                             var_name="Status",
                                             value_name="Count")

        # Display the processed dataset
        display(data_counts)

        return data_counts

    def process_field_data(self):
        df_subset = self.data[['Species', 'Plot']]
        contingency_table = pd.crosstab(df_subset['Plot'], df_subset['Species'])

        df_final = pd.DataFrame(contingency_table)

        # Display the processed dataset
        display(df_final)

        return df_final

    def process_light_level_data(self):
        df_sublight = self.data[['Light_Cat', 'Alive', 'Event']]
        df_sublight['Alive'] = df_sublight['Alive'].replace('X', 1)
        df_sublight['Alive'] = df_sublight['Alive'].fillna(0)
        df_sublight = df_sublight.rename(columns={'Event': 'Dead'})

        by_light_df = df_sublight.groupby('Light_Cat').sum()

        light_cat = ["High", "Low", "Med"]
        by_light_df.insert(0, 'Light_Cat', light_cat)

        light_df = pl.DataFrame(by_light_df)

        # Ensure 'Alive' column is present in the light_df DataFrame
        if 'Alive' not in light_df.columns:
            light_df['Alive'] = 0

        if 'Dead' not in light_df.columns:
            light_df['Dead'] = 1

        # Convert Polars DataFrame to Pandas DataFrame
        light_pandas_df = light_df.to_pandas()

        data_light_counts = light_pandas_df.melt(id_vars="Light_Cat",
                                                 value_vars=["Alive"],
                                                 var_name="Status",
                                                 value_name="Count")

        # Display the processed dataset
        display(data_light_counts)

        return data_light_counts

        # Display the processed dataset
        display(data_light_counts)

        return data_light_counts

# Example usage:
# tree_cleaner = TreeDataCleaner(data)

# Process and view datasets for each function
# raw_cleaned = tree_cleaner.cleaned_data()
# species_data = tree_cleaner.process_species_data()
# field_data = tree_cleaner.process_field_data()
# light_level_data = tree_cleaner.process_light_level_data()
