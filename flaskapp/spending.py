import getpass
import sqlite3
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine, exc


class Spending_History():

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def spending_history_webpage(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-extensions")

        mydriver = webdriver.Chrome(
            executable_path='chromedriver', chrome_options=options)
        mydriver.get("https://get.cbord.com/gwu/full/login.php")

        # print("Logging in...")

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

        # print("Extracting spending history...")

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
        df.sort_values(by='date', inplace=True)
        df = df.reset_index(drop=True)
        df.index.names = ['id']

        df['email'] = self.email

        # print("Adding to database...")

        disk_engine = create_engine('sqlite:///test.db')
        for i in range(len(df)):
            try:
                df.iloc[i:i + 1].to_sql(name="history",
                                        if_exists='append', con=disk_engine)
            except exc.IntegrityError:
                pass

        return df

