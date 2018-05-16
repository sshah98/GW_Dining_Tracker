import getpass
import pickle
import sqlite3

import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from sqlalchemy import create_engine


myuser = input('Enter username: ')
mypass = getpass.getpass('Enter password: ')
baseurl = "https://get.cbord.com/gwu/full/login.php"


def spending_history_webpage():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-extensions")

    mydriver = webdriver.Chrome(
        executable_path='chromedriver', chrome_options=options)
    mydriver.get(baseurl)

    print("Logging in...")

    mydriver.find_element_by_id(
        "login_username_text").send_keys(myuser)
    mydriver.find_element_by_id(
        "login_password_text").send_keys(mypass)
    mydriver.find_element_by_name("submit").click()

    mydriver.get("https://get.cbord.com/gwu/full/history.php")
    html = mydriver.page_source
    soup = BeautifulSoup(html, "lxml")

    mydriver.close()

    return soup


def webpage_to_dataframe():

    soup = spending_history_webpage()
    table = soup.find("table", {"class": "table table-striped table-bordered"})

    print("Extracting spending history...")

    # removes commas and more necessary formatting
    items = list(table.stripped_strings)
    # gets after 4 b/c 1st 4 headers Cash, Datetime, Price, Vendor
    items = [elem for elem in items if elem.strip(",")]
    items = items[4:]
    items = [items[i:i + 5] for i in range(0, len(items), 5)]

    # create a dataframe
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

    df.sort_values(by='date', inplace=True)
    df.set_index('date', inplace=True)

    print("Saving to csv file...")

    myfile = '%s' % (myuser.strip('@gwmail.gwu.edu')) + '_gworld_dollars.csv'
    df.to_csv(myfile)

    print("Adding to database...")

    disk_engine = create_engine('sqlite:///spending_history.db')
    df.to_sql('history', disk_engine, if_exists='append')

    return df


# webpage_to_dataframe()
