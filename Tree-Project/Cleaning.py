import pandas as pd

data = pd.read_csv('../example/Tree_Data.csv')

# Check for missing values in each column
print(data.isnull().sum())

