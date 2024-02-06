import pandas as pd


def import_data():

    df = pd.read_csv("../example/Tree_Data.csv")
    return df
