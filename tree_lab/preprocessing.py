from sklearn.preprocessing import *
import pandas as pd


class DataPreprocessor:
    """
    A class for preprocessing data.

    Parameters:
        - data: pandas.DataFrame
    """

    def __init__(self, data):
        """
        Initializes the DataPreprocessor object.

        Parameters:
        - data (pandas.DataFrame): The input data for preprocessing.
        """

        self.data = data.copy()

    def normalize_data(self, numeric_columns, scaler_type="normal"):
        """
        Normalizes the numeric columns of the input data using the specified
        scaler type.

        Parameters:
            - numeric_columns (list): list of column names containing numeric data
            to be normalized.

            - scaler_type (str): the type of scaler to be used.
            Options: 'normal' (default), 'minmax', 'max_absolute'.

        Returns:
            pandas.DataFrame: the normalized data.

        Raises:
        ValueError, if the specified columns are not numeric or contain NA values.
        """

        stop = False
        numeric_data = self.data[numeric_columns]

        for col in numeric_columns:
            if not (pd.to_numeric(numeric_data[col],
                                  errors='coerce').notnull().all()):
                print(
                    f"'{col}' is not a numeric column! "
                    f"It is either categorical or contains n/a values! "
                    f"Only numeric columns can be normalized!")
                stop = True
                break

        if not stop:
            if scaler_type == "minmax":
                scaler = MinMaxScaler()

            elif scaler_type == "normal":
                scaler = StandardScaler()

            elif scaler_type == "max_absolute":
                scaler = MaxAbsScaler()
            else:
                scaler = MinMaxScaler()

            normalized_data = scaler.fit_transform(numeric_data)
            self.data[numeric_columns] = normalized_data

            return self.data

    def onehot_encode(self, columns, keep_original=True):
        """
        Performs one-hot encoding on specified columns of the input data.

        Parameters:
            - columns (list): list of column names containing categorical data
            to be one-hot encoded.
            - keep_original (bool): if True, keeps the original columns in addition
            to the one-hot encoded columns.

        Returns:
            pandas.DataFrame: the one-hot encoded data.

        Raises:
        ValueError, if the specified columns are not of type 'object'.
        """

        proceed = True
        for col in columns:
            if not (self.data[col].dtype == 'object'):
                proceed = False
                print("One of the inputted columns is maybe not an Object!")
                break

        if proceed:

            onehot_data = pd.get_dummies(self.data, columns=columns)

            if keep_original:
                subset = self.data[columns]
                self.data = pd.concat([onehot_data, subset], axis=1)

                return self.data

            self.data = onehot_data

            return self.data

    def display(self):
        """

        Returns:
            pandas.DataFrame: the current state of the data.
        """

        return self.data
