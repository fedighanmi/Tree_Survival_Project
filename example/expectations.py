# here we write the functions that we want to test :)

def normalize_data(self, numeric_columns, scaler_type="normal"):
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

# test for another function with means and sd for example