import os

import numpy as np
import pandas as pd
import psycopg2

from spending import SpendingHistory
from models import *

DATABASE_URL = os.environ['DATABASE_URL']
database = psycopg2.connect(DATABASE_URL, sslmode='allow')

data = User.query.filter_by(email=session['email']).first()

if data.kitchen == "yes":
    initial_gworld = 1400

elif data.kitchen == "no":
    initial_gworld = 2600
else:
    initial_gworld = 1350
without_kitchen = 2300
with_kitch = 1400

df = pd.read_sql_query(
    "SELECT * FROM history WHERE email='%s'" % ('suraj98@gwu.edu'), database)
df['currentval'] = np.nan
df['currentval'] = df['price'] - df['currentval']
df.currentval = initial_gworld + df.price.cumsum()
df.drop(columns=['date', 'time'], inplace=True)

df.set_index('datetime', inplace=True)


print(df.head())
