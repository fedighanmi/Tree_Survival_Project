import pandas as pd

data = pd.read_csv('../example/Tree_Data.csv')

# Data Cleaning and Feature Engineering
data = data.drop(['Plot', 'Subplot', 'Time', 'Event', 'Harvest'], axis=1)

# Handle missing values
data['EMF'].fillna(data['EMF'].mean(), inplace=True)

# Check for any null values
data.any().isnull()

# Remove duplicate rows in the dataset
data = data.drop_duplicates()
