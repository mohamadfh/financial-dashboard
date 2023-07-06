import pandas as pd
import threading
import datetime
import hermes
import os
import dbcontrollers
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

dbconn = dbcontrollers.init_connection(os.environ.get("DATABASE"),os.environ.get("USER"),os.environ.get("PASSWORD"),os.environ.get("HOST"),int(os.environ.get("PORT")))
if dbconn is not None:
    dbcontrollers.add_table(dbconn,"fundsindices","value FLOAT, datetime TIMESTAMP")
    dbcontrollers.add_table(dbconn,"totalindices","value FLOAT, datetime TIMESTAMP")

total_index_df = pd.DataFrame(columns=['value', 'datetime'])
funds_index_df = pd.DataFrame(columns=['value', 'datetime'])


def execute_within_time_interval(start_time, end_time):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_time = datetime.datetime.now().time()

            if start_time <= current_time <= end_time:
                return func(*args, **kwargs)
            else:
                pass

        return wrapper

    return decorator


#@execute_within_time_interval(datetime.time(9, 0), datetime.time(12, 30))
def update_dfs():
    time = datetime.datetime.now()
    start_time = datetime.time(9, 0)
    end_time = datetime.time(12, 30)

    if start_time <= time.time() <= end_time:
        global total_index_df
        global funds_index_df
        time = datetime.datetime.now()
        stock_df = hermes.Market_with_askbid()
        total_index = calc_total_index(stock_df)
        funds_index = calc_funds_index(stock_df)
        total_new_data = {'datetime': time, 'value': total_index}
        funds_new_data = {'datetime': time, 'value': funds_index}
        total_index_df.loc[len(total_index_df)] = total_new_data
        funds_index_df.loc[len(funds_index_df)] = funds_new_data
        #store in db:
        if dbconn is not None:

            cursor = dbconn.cursor()
            insert_query = "INSERT INTO totalindices (value, datetime) VALUES (%s, %s);".format()
            cursor.execute(insert_query, (total_index, time))
            dbconn.commit()
            insert_query = "INSERT INTO fundsindices (value, datetime) VALUES (%s, %s);".format()
            cursor.execute(insert_query, (funds_index, time))
            dbconn.commit()
            cursor.close()


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
