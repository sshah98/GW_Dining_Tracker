from bs4 import BeautifulSoup

from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException

# import pickle
import getpass

import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

import datetime as dt

from sklearn.linear_model import LinearRegression


plt.style.use('fivethirtyeight')


def login():

    myuser = input('Enter netID (no gwu.edu): ') + '@gwu.edu'
    mypass = getpass.getpass('Password: ')

    baseurl = "https://get.cbord.com/gwu/full/login.php"

    mydriver = webdriver.Firefox()
    mydriver.get(baseurl)

    # clearuser = mydriver.find_element_by_id("login_username_text").clear()
    # clearpass = mydriver.find_element_by_id("login_password_text").clear()

    # TODO: Debug if password or username is not correct:

    username = mydriver.find_element_by_id("login_username_text")
    password = mydriver.find_element_by_id("login_password_text")

    username.send_keys(myuser)
    password.send_keys(mypass)

    mydriver.find_element_by_name("submit").click()

    mydriver.get("https://get.cbord.com/gwu/full/history.php")

    html = mydriver.page_source
    soup = BeautifulSoup(html, "lxml")

    mydriver.close()

    # used pickle for debugging while getting table and converting to dataframe
    # with open('site.pickle', 'wb') as handle:
    #     pickle.dump(soup, handle, protocol=pickle.HIGHEST_PROTOCOL)
    # with open('site.pickle', 'rb') as handle:
    #     b = pickle.load(handle)

    table = soup.find("table", {"class": "table table-striped table-bordered"})

    # adds all table rows
    rows = list()
    for row in table.findAll("tr"):
        rows.append(row)

    # removes commas and more necessary formatting
    items = list(table.stripped_strings)
    items = [elem for elem in items if elem.strip(",")]

    # gets after 4, because the first four are the headers - Cash, Datetime, Price, Vendor
    items = items[4:]
    items = [items[i:i + 5] for i in range(0, len(items), 5)]

    # create a dataframe
    df = pd.DataFrame(items)

    # converts Dining Cash to string instead of object
    df[0] = df[0].astype(str)

    # fix prices (removes -, $) and converts to float
    df[4] = df[4].str.replace('$', '')
    df[4] = df[4].str.replace('- ', '')
    df[4] = df[4].str.replace('+', '')
    df[4] = df[4].astype(float)

    # converts day, month, year to proper date format
    df[1] = pd.to_datetime(df[1], errors='coerce')

    # converts time to proper time format
    df[2] = pd.to_datetime(df[2])
    df[2] = df[2] = pd.Series([val.time() for val in df[2]])

    # converts place to string
    df[3] = df[3].astype(str)

    df = df.rename(columns={0: 'Account', 1: 'Date',
                            2: 'Time', 3: 'Vendor', 4: 'Price'})

    myfile = '%s' % myuser.strip('@gwu.edu') + '_gworld_dollars.csv'
    df.to_csv(myfile)


# login()

def analysis():

    # read csv file and format for proper usage
    df = pd.read_csv('suraj98_gworld_dollars.csv', parse_dates=['Date'])
    df = df.sort_values(by='Date')
    df.set_index('Date', inplace=True)

    df1 = df.truncate(before='2018-01-06')
    df1['CurrentVal'] = 0
    # df1['Current Value'] = df1['Price'] - df1['Current Value']
    df1.CurrentVal = 1350 * 2 - df1.Price.cumsum()

    df1.rename(columns={'Unnamed: 0': 'Count'}, inplace=True)
    del df1['Count']

    print(df1.head())

    plt.figure()

    x = df1.index
    y = df1['CurrentVal']

    plt.plot(x, y, 'ko')

    df1.index = pd.to_datetime(df1.index)
    df1.index = df1.index.map(dt.datetime.toordinal)

    x1 = df1.index
    m, b = np.polyfit(x1, y, 1)
    plt.plot(x1, m * x1 + b, '-')

    plt.ylim(ymin=0)
    plt.xticks(rotation='vertical')
    plt.xlabel('Date')
    plt.ylabel('CurrentVal')

    plt.show()

    # plt.savefig('spending.png', bbox_inches='tight')


analysis()
