import pytest
import pytest
import pandas as pd
from tree_lab import preprocessing as prp

def test_normalize():
    pass


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





