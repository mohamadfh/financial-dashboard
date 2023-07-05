import pandas as pd
import numpy as np
from hermes import Market_with_askbid
from typing import Union

def total_index(df: pd.DataFrame) -> float:
    weighted_sum = (df['last_return'] * df['value']).sum()
    total_weight = df['value'].sum()
    weighted_average = weighted_sum / total_weight
    return weighted_average

def filter_funds(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['isin'].str.startswith('IRT')]

if __name__ == "__main__":
    df = Market_with_askbid()
    print("fetched")
    print(total_index(df))
    print(total_index(filter_funds(df)))