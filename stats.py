import math
import sqlite3
import datetime
import pandas as pd
import numpy as np

# from sklearn import preprocessing, cross_validation, svm
# from sklearn.linear_model import LinearRegression

# from sklearn.cross_validation import train_test_split
# import statsmodels.api as sm


initial_gworld = 1350

import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='require')
# import matplotlib.pyplot as plt

def graphed_spending():

    df = pd.read_sql_query("SELECT * FROM history", database)

    # formatting and making information from database clean
    df['currentval'] = np.nan
    df['currentval'] = df['price'] - df['currentval']
    df.currentval = initial_gworld + df.price.cumsum()
    df.set_index('datetime', inplace=True)

    # print(df.to_string())
    
    

    return df


# graphed_spending()

# df['date'] = pd.to_datetime(df['date'])
# df['date_delta'] = (df['date'] - df['date'].min())  / np.timedelta64(1,'D')
# xdat = df['date_delta']
# xdat = sm.add_constant(xdat)
# xdat = sm.add_constant(xdat)
# ydat = df['currentval']
# model = sm.OLS(ydat,xdat)
# result = model.fit()
# print(result.params)
# print(result.summary())
# print('Predicted values: ', result.predict())
