import sqlite3

import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import datetime as dt


import math
import datetime
import pickle
import matplotlib.pyplot as plt

from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression
from matplotlib import style

style.use('ggplot')

initial_gworld = 1350

DATABASE = 'spending_history.db'

db = sqlite3.connect(DATABASE)
df = pd.read_sql_query("SELECT * FROM history", db)

df['currentval'] = np.nan
df['currentval'] = df['price'] - df['currentval']
df.currentval = initial_gworld + df.price.cumsum()

df['datetime'] = pd.to_datetime(df['date'].apply(str) + ' ' + df['time'])
df.set_index('count', inplace=True)


print(df.head())

df.plot(x='datetime', y='currentval')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()



# x = df.index
# y = df['CurrentVal']
#
# print("Plotting and calculating stats...")
#
# plt.scatter(x, y)
#
#
# df.index = pd.to_datetime(df.index)
# df.index = df.index.map(dt.datetime.toordinal)
#
# x1 = df.index
# m, b = np.polyfit(x1, y, 1)
#
# plt.plot(x1, m * x1 + b, '-')
#
# predicted_date = int(-b / m)
# predicted_date = dt.datetime.fromordinal(predicted_date).date()
# print("Predicted to run out: " + str(predicted_date))
#
# print("Spending on average per day: $" + str(round(abs(m), 2)))
#
# plt.ylim(ymin=0)
# plt.xticks(rotation='vertical')
# plt.xlabel('Date')
# plt.ylabel('CurrentVal')


# plt.show()
