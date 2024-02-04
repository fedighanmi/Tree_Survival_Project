import pytest
import pandas as pd
from tree_lab import preprocessing as prp

df = pd.read_csv("../example/Tree_Data.csv")

def test_normalize():
    pass


def min_max_normalization(column):
    # Find the minimum and maximum values in the column
    min_val = min(df[column])
    max_val = max(df[column])

    # Normalize each value in the column
    norm_col = pd.Series([(x - min_val) / (max_val - min_val) for x in column])

    return norm_col

@pytest.fixture
def sample_cols():
    cols = ["Light_ISF", "Lignin"]
    return cols

def test_data(sample_cols):
    for col in sample_cols:
        processed_data = min_max_normalization(col)
        assert processed_data.tolist() == pytest.approx(prp.DataPreprocessor.normalize_data(
            numeric_columns=col, scaler_type="minmax").tolist(), abs=1e-5)

# Assume you have a function that processes a DataFrame
def process_data(df):
    # Some processing logic on two columns
    df['result'] = df['column1'] + df['column2']
    return df


# Fixture to create a sample DataFrame
@pytest.fixture
def sample_data():
    data = {'column1': [1, 2, 3],
            'column2': [4, 5, 6]}
    return pd.DataFrame(data)


# Test case to check if the result column is calculated correctly
def test_process_data(sample_data):
    processed_data = process_data(sample_data)
    l = [5, 7, 9]
    # Check if the 'result' column is calculated correctly
    assert processed_data['result'].tolist() == pytest.approx(l, abs=1e-2)