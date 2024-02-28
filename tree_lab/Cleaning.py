class TreeDataCleaner:
    """
    Initializes a TreeDataCleaner object.

    Parameters:
        data (pandas.DataFrame): The input pandas DataFrame containing tree data.
    """

    def __init__(self, data):
        self.data = data.copy()

    def detect_na(self):
        """

        Checks for null values in the dataset, prints columns with null values (if any),
        and removes duplicate rows in the dataset.
        """

        # Check for any null values in the dataset
        null_values_check = self.data.isnull().any()

        # Print columns with null values, if any
        if null_values_check.any():
            print("Columns with null values:")
            print(null_values_check[null_values_check].index.tolist())

        # Remove duplicate rows in the dataset
        self.data = self.data.drop_duplicates()

    def impute_na(self):
        """
        Imputes missing values in the 'EMF' column by filling them with the mean of the column.
        Fills any remaining null values in the dataset with 0.
        """

        self.data['EMF'].fillna(self.data['EMF'].mean(), inplace=True)
        self.data = self.data.fillna(0)

    def modify_status(self):
        """
        Modifies the 'Alive' column by replacing 'X' with 1.
        Renames the 'Event' column to 'Dead'.

        Returns:
            pandas.DataFrame: The modified DataFrame.

        """
        self.data['Alive'] = self.data['Alive'].replace('X', 1)
        self.data = self.data.rename(columns={'Event': 'Dead'})

        return self.data

    def del_cols(self, columns_to_delete):
        """
        Function to allow users to delete specified columns.

        Parameters:
        - columns_to_delete: A list of column names to be deleted.

        Example:
        cleaner.del_cols(['Age', 'Height'])
        """

        for column_name in columns_to_delete:
            if column_name in self.data.columns:
                del self.data[column_name]
            else:
                print(f"Column '{column_name}' either already deleted or not found in the dataset.")

    def display(self):
        """

        Returns:
        pandas.DataFrame: The current state of the data.
        """

        return self.data
