import sqlite3

import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import datetime as dt

# myuser = input('Enter username: ')
# mypass = getpass.getpass('Enter password: ')
# baseurl = "https://get.cbord.com/gwu/full/login.php"
# user = myuser.strip('@gwmail.gwu.edu')

initial_gworld = 1350

# myfile = '%s' % (myuser.strip('@gwmail.gwu.edu')) + '_gworld_dollars.csv'

DATABASE = 'spending_history.db'

db = sqlite3.connect(DATABASE)

df = pd.read_sql_query("SELECT * FROM history", db)

# remove first row which has the labels
# df=df.iloc[1:]
        
print(df.head())
# 
# print("Reading information...")
# df = pd.read_csv(myfile, parse_dates=['Date'])
# df = df.sort_values(by='Date')
# df.set_index('Date', inplace=True)
# 
# # df = df.truncate(before='2018-01-06')
# df['CurrentVal'] = np.nan
# # df['Current Value'] = df['Price'] - df['Current Value']
# df.CurrentVal = initial_gworld - df.Price.cumsum()
# 
# del df['Count']
# 
# print(df)
# 
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