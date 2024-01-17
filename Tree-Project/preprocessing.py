from sklearn.preprocessing import MinMaxScaler


class DataPreprocessor:

    def __init__(self, data):
        self.data = data.copy()
        self.scaler = MinMaxScaler()

    def normalize_data(self, numeric_columns):
        numeric_data = self.data[numeric_columns]
        normalized_data = self.scaler.fit_transform(numeric_data)
        self.data[numeric_columns] = normalized_data
        return self.data

