from sklearn.preprocessing import *
import pandas as pd


class DataPreprocessor:

    def __init__(self, data):
        self.data = data.copy()

    def normalize_data(self, numeric_columns, scaler_type="normal"):
        stop = False
        numeric_data = self.data[numeric_columns]

        for col in numeric_columns:
            if not (pd.to_numeric(numeric_data[col], errors='coerce').notnull().all()):
                print(
                    f"'{col}' is not a numeric column! It is either categorical or contains n/a values! "
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

        return self.data
