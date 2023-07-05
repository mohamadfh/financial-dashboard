import pandas as pd
import numpy as np
from hermes import Market_with_askbid
from typing import Union
import threading
import time 
import datetime
import hermes

dft = pd.DataFrame(columns=['index', 'time'])
dff = pd.DataFrame(columns=['index', 'time'])

def update_df():
    global dft
    global dff
    time = datetime.datetime.now().strftime('%H:%M:%S')
    stock_df = hermes.Market_with_askbid()
    ti = calc_total_index(stock_df)
    fi = calc_funds_index(stock_df)
    new_data_total = {'time': time, 'index': ti}
    new_data_fund = {'time': time, 'index': fi}

    dft.loc[len(dft)] = new_data_total
    dff.loc[len(dff)] = new_data_fund


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec) 
        func()  
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def calc_total_index(df: pd.DataFrame) -> float:
    last_return = df['last_return'].astype(float)
    value = df['value'].astype(float)
    weighted_avg = (last_return * value).sum() / value.sum()
    return weighted_avg

def filter_funds(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['isin'].str.startswith('IRT')]

def calc_funds_index(df: pd.DataFrame) -> float:
    return calc_total_index(filter_funds(df))


