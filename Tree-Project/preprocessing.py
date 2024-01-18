from sklearn.preprocessing import MinMaxScaler, StandardScaler, MaxAbsScaler
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
                    f"'{col}' is not a numeric column! It is either categorical or "
                    f"containes n/a values! Only numeric columns can be normalized!")
                stop = True
                break

        if not (stop):
            if scaler_type == "minmax":
                scaler = MinMaxScaler()

            elif scaler_type == "normal":
                scaler = StandardScaler()

            elif scaler_type == "max_absolute":
                scaler = MaxAbsScaler()

            normalized_data = scaler.fit_transform(numeric_data)
            self.data[numeric_columns] = normalized_data

            return self.data


