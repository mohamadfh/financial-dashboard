import pandas as pd
import numpy as np
from hermes import Market_with_askbid
from typing import Union

def calc_index(df: pd.DataFrame) -> float:
    last_return = df['last_return'].astype(float)
    value = df['value'].astype(float)
    weighted_avg = (last_return * value ).sum() / value.sum()
    return weighted_avg

def filter_funds(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['isin'].str.startswith('IRT')]

if __name__ == "__main__":
    df = Market_with_askbid()
    print("fetched")
    print(calc_index(df))
    print(calc_index(filter_funds(df)))