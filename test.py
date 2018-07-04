import os
import psycopg2
import datetime

import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn import preprocessing, cross_validation, svm

from models import *

database = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='allow')

data = User.query.filter_by(email='suraj98@gwu.edu').first()

predicted_days = 7

if data.kitchen == "yes":
    initial_gworld = 1400

elif data.kitchen == "no":
    initial_gworld = 2600
else:
    initial_gworld = 1350


df = pd.read_sql_query(
    "SELECT * FROM history WHERE email='%s'" % ('suraj98@gwu.edu'), database)
df['currentval'] = np.nan
df['currentval'] = df['price'] - df['currentval']
df.currentval = initial_gworld + df.price.cumsum()

df.drop(columns=['date', 'time'], inplace=True)
df.set_index('datetime', inplace=True)

df = df[['currentval']]

# predicting 30 days into future
forecast_out = int(predicted_days)

# label column with data shifted 30 units up
df['Prediction'] = df[['currentval']].shift(-forecast_out)

X = np.array(df.drop(['Prediction'], 1))
X = preprocessing.scale(X)

# set X_forecast equal to last 30
X_forecast = X[-forecast_out:]
# remove last 30 from X
X = X[:-forecast_out]
y = np.array(df['Prediction'])
y = y[:-forecast_out]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(
    X, y, test_size=0.2)

clf = LinearRegression()
clf.fit(X_train, y_train)

# Testing
confidence = clf.score(X_test, y_test)
forecast_prediction = clf.predict(X_forecast)

print("confidence: ", confidence)
print(forecast_prediction)

future_days_list = []

for i in range(1, predicted_days+1):
    future_days_list.append(df.tail(1).index + datetime.timedelta(days=i))


predicted_df = pd.DataFrame(future_days_list)

forecast = pd.Series(forecast_prediction)
predicted_df['currentval'] = forecast.values

predicted_df.columns = ['datetime', 'price']
predicted_df.set_index('datetime', inplace=True)


print(predicted_df)

# newlist = list(zip(forecast_prediction, mylist))
# 
# 
# print(df)

# import matplotlib.pyplot as plt
# plt.plot(forecast_prediction)
# plt.ylabel('Price')
# plt.xlabel('Days')
# plt.show()
