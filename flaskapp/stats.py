import math
import sqlite3
import datetime
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt

# from sklearn import preprocessing, cross_validation, svm
# from sklearn.linear_model import LinearRegression
from matplotlib import style

# from sklearn.cross_validation import train_test_split
# import statsmodels.api as sm

# style.use('ggplot')

initial_gworld = 1350
database = 'test.db'


def graphed_spending():

    db = sqlite3.connect(database)
    df = pd.read_sql_query("SELECT * FROM history", db)

    # formatting and making information from database clean
    df['currentval'] = np.nan
    df['currentval'] = df['price'] - df['currentval']
    df.currentval = initial_gworld + df.price.cumsum()
    df['datetime'] = pd.to_datetime(df['date'].apply(str) + ' ' + df['time'])
    # df['date'] = pd.to_datetime(df['date']).dt.date
    df.set_index('datetime', inplace=True)
        
    return df
    # plt.scatter(df['datetime'].tolist(), df['currentval'])
    # plt.xlabel('Date')
    # plt.ylabel('GWorld')
    #
    # plt.show()


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
