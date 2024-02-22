import pandas as pd


def import_data():
    try:
        df = pd.read_csv("example/Tree_Data.csv")
    except FileNotFoundError:
        df = pd.read_csv("../example/Tree_Data.csv")
    return df


