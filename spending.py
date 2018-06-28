import pandas as pd
import numpy as np
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine, exc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# --- heroku --- #
CHROMEDRIVER_PATH = os.environ['CHROMEDRIVER_PATH']
GOOGLE_CHROME_BIN = os.environ['GOOGLE_CHROME_BIN']

class SpendingHistory():

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def spending_history(self):

        try:

            options = Options()

            # --- heroku --- #
            options.binary_location = GOOGLE_CHROME_BIN

            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument("--disable-extensions")

            # --- local testing --- #
            # driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

            # --- heroku --- #
            driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)

            print("opening chrome")

            driver.get("https://get.cbord.com/gwu/full/login.php")
            driver.find_element_by_id(
                "login_username_text").send_keys(self.email)
            driver.find_element_by_id(
                "login_password_text").send_keys(self.password)
            driver.find_element_by_name("submit").click()
            driver.get("https://get.cbord.com/gwu/full/history.php")

            soup = BeautifulSoup(driver.page_source, "lxml")
            driver.close()

            print("found data")

            try:
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

                print("creating dataframe")

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

                # --- local testing --- #
                # engine = create_engine("postgresql://suraj:password@localhost/gworld")

                # --- heroku --- #
                engine = create_engine("postgresql+psycopg2://gvbgcpweihoipq:d52e382574f9ad2313c882534fb07ceb52484e04f112b3e405c3e9ee441048b2@ec2-54-235-206-118.compute-1.amazonaws.com:5432/d4n9qk3lo1qsr2")

                for i in range(len(df)):
                    try:
                        df.iloc[i:i + 1].to_sql(name="history",
                                                if_exists='append', con=engine)
                    except exc.IntegrityError:
                        pass

                print("data collected")

            except AttributeError as e:
                print("wrong username/password")

        except NoSuchElementException as e:
            print("No internet connection")
            
