import pandas as pd
import numpy as np
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine, exc

# CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
# GOOGLE_CHROME_BIN = os.environ['GOOGLE_CHROME_BIN']

class Spending_History():

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def spending_history_webpage(self):
        options = Options()
        # options.binary_location = GOOGLE_CHROME_BIN
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument("--disable-extensions")

        mydriver = webdriver.Chrome(
            executable_path="/home/suraj/Documents/Programming/current-projects/GW_Dining_Tracker/chromedriver", chrome_options=options)

        mydriver.get("https://get.cbord.com/gwu/full/login.php")
        mydriver.find_element_by_id(
            "login_username_text").send_keys(self.email)
        mydriver.find_element_by_id(
            "login_password_text").send_keys(self.password)
        mydriver.find_element_by_name("submit").click()
        mydriver.get("https://get.cbord.com/gwu/full/history.php")
        html = mydriver.page_source
        soup = BeautifulSoup(html, "lxml")
        mydriver.close()

        return soup

    def webpage_to_dataframe(self):

        soup = self.spending_history_webpage()
        table = soup.find(
            "table", {"class": "table table-striped table-bordered"})

        # formatting before converting to dataframe
        items = list(table.stripped_strings)
        items = [elem for elem in items if elem.strip(",")]
        items = items[4:]
        items = [items[i:i + 5] for i in range(0, len(items), 5)]

        # more cleaning data
        df = pd.DataFrame(items)
        df = df.astype(str)
        df[4] = df[4].replace({'\$': '', '\+ ': '', '- ': '-'}, regex=True)
        df[4] = df[4].astype(np.float64)

        # converts day, month, year time to proper format
        df[1] = pd.to_datetime(df[1], errors='raise')
        df[2] = pd.to_datetime(df[2], errors='raise')
        df[2] = df[2] = pd.Series([val.time() for val in df[2]])

        df = df.rename(columns={0: 'account', 1: 'date',
                                2: 'time', 3: 'vendor', 4: 'price'})

        # sort values by date and reset the index for the count, which is PK
        df = df.reset_index(drop=True)
        df.index.names = ['id']

        df['email'] = self.email

        df['datetime'] = pd.to_datetime(
            df['date'].apply(str) + ' ' + df['time'].apply(str))

        df.drop(columns=['date', 'time'], inplace=True)
        df.sort_values(by='datetime', inplace=True, ascending=True)

        # print(df.to_string())

        disk_engine = create_engine(
            'postgresql+psycopg2://gvbgcpweihoipq:d52e382574f9ad2313c882534fb07ceb52484e04f112b3e405c3e9ee441048b2@ec2-54-235-206-118.compute-1.amazonaws.com:5432/d4n9qk3lo1qsr2')
        for i in range(len(df)):
            try:
                df.iloc[i:i + 1].to_sql(name="history",
                                        if_exists='append', con=disk_engine)
            except exc.IntegrityError:
                pass

        return df
