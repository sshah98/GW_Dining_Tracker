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


class SpendingHistory():

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def spending_history(self):

        try:

            options = Options()

            # --- heroku --- #
            options.binary_location = os.environ['GOOGLE_CHROME_BIN']

            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument("--disable-extensions")

            # --- local testing --- #
            # driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

            # --- heroku --- #
            driver = webdriver.Chrome(executable_path=os.environ['CHROMEDRIVER_PATH'], chrome_options=options)

            print("[INFO] Opening browser...")

            driver.get("https://get.cbord.com/gwu/full/login.php")
            driver.find_element_by_id(
                "login_username_text").send_keys(self.email)
            driver.find_element_by_id(
                "login_password_text").send_keys(self.password)
            driver.find_element_by_name("submit").click()
            driver.get("https://get.cbord.com/gwu/full/history.php")

            soup = BeautifulSoup(driver.page_source, "lxml")
            driver.close()

            print("[INFO] Closing browser, found data...")

            try:

                table = soup.find('div', class_='history_table table-responsive')

                print("[INFO] Creating dataframe...")
                
                df = pd.read_html(table.prettify())[0]
                df['Amount ($ / Meals)'] = df['Amount ($ / Meals)'].replace({'\$': '', '\+ ': '', '- ': '-'}, regex=True)
                df['Date & Time'] = pd.to_datetime(df['Date & Time'])
                
                print('[INFO] Cleaning data...')
                df.dropna(inplace=True)
                df.columns = ['account', 'datetime', 'vendor', 'price']
                df['price'] = df['price'].astype(np.float64)
                df = df.reset_index(drop=True)
                df.index.names = ['id']
                df['email'] = self.email
                df.sort_values(by='datetime', inplace=True, ascending=True)
                
                
                # # --- local testing --- #
                # engine = create_engine("postgresql://suraj:password@localhost/gworld")

                # --- heroku --- #
                engine = create_engine("postgresql+psycopg2://gefimacpqdfbke:07654d71914a5e524f41fb4b9cb31e8f1e9ba4ba9f7676bcd4afadf1caa9e5c5@ec2-50-16-217-122.compute-1.amazonaws.com:5432/d6ncrb2kqoer99")

                print('[INFO] Storing in database...')
                
                for i in range(len(df)):
                    try:
                        df.iloc[i:i + 1].to_sql(name="history",
                                                if_exists='append', con=engine)
                    except exc.IntegrityError:
                        pass

                print("[INFO] Finished collecting data...")
                
            except AttributeError as e:
                print("Wrong username/password")
        except NoSuchElementException as e:
            print("No internet connection")