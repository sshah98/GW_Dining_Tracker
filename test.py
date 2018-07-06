import os
import psycopg2
import datetime

import pandas as pd
import numpy as np

df = pd.read_csv('vendorInformation/diningVendors.csv')
print(df.head())
