import pandas as pd

data = pd.read_csv('../example/Tree_Data.csv')


class TreeDataCleaner:
    def __init__(self, data):
        self.data = data

    def detect_na(self):
        # Check for any null values in the dataset
        null_values_check = self.data.isnull().any()

        # Print columns with null values, if any
        if null_values_check.any():
            print("Columns with null values:")
            print(null_values_check[null_values_check].index.tolist())

        # Remove duplicate rows in the dataset
        self.data = self.data.drop_duplicates()

    def impute_na(self):
        self.data['EMF'].fillna(self.data['EMF'].mean(), inplace=True)
        self.data = self.data.fillna(0)

    def modify_status(self):
        self.data['Alive'] = self.data['Alive'].replace('X', 1)
        self.data = self.data.rename(columns={'Event': 'Dead'})

        return self.data

    def input_values(self, columns_to_delete):
        """
        Function to allow users to delete specified columns.

        Parameters:
        - columns_to_delete: A list of column names to be deleted.

        Example:
        cleaner.input_values(['Age', 'Height'])
        """
        for column_name in columns_to_delete:
            if column_name in self.data.columns:
                del self.data[column_name]
            else:
                print(f"Column '{column_name}' not found in the dataset.")

        return self.data

