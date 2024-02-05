import pytest
import pandas as pd
from tree_lab import preprocessing as prp


df = pd.read_csv("../example/Tree_Data.csv")
data_prep = prp.DataPreprocessor(df)


def min_max_normalization(column):
    # Find the minimum and maximum values in the column
    min_val = min(column)
    max_val = max(column)

    # Normalize each value in the column
    norm_col = pd.Series([(x - min_val) / (max_val - min_val) for x in column])

    return norm_col

""" 
@pytest.mark.parametrize("col", ["Lignin", "Light_ISF", "AMF", "NSC"])
def test_minmax(col):
    assert min_max_normalization(df[col]).all() == pytest.approx(
        data_prep.normalize_data([col], "mixmax")[col].all(), abs=1e-4)
"""
