import getpass
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import datetime as dt

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select
# from selenium.common.exceptions import NoSuchElementException

plt.style.use('fivethirtyeight')

# myuser = input('Enter username: ')
# mypass = getpass.getpass('Enter password: ')
baseurl = "https://get.cbord.com/gwu/full/login.php"
# user = myuser.strip('@gwmail.gwu.edu')


class DiningDollars(object):

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def loginToAccount(self):
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-extensions")
        

        mydriver = webdriver.Chrome(
            executable_path='/usr/local/bin/chromedriver', chrome_options=options)
        mydriver.get(baseurl)

        print("Logging in...")
        mydriver.find_element_by_id("login_username_text").send_keys(self.login)
        mydriver.find_element_by_id("login_password_text").send_keys(self.password)
        mydriver.find_element_by_name("submit").click()
        
        mydriver.get("https://get.cbord.com/gwu/full/history.php")

        html = mydriver.page_source
        soup = BeautifulSoup(html, "lxml")

        mydriver.close()

        return soup
        
    def dailyTransactions(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-extensions")
        

        mydriver = webdriver.Chrome(
            executable_path='/usr/local/bin/chromedriver', chrome_options=options)
        mydriver.get(baseurl)

        print("Logging in...")
        mydriver.find_element_by_id("login_username_text").send_keys(self.login)
        mydriver.find_element_by_id("login_password_text").send_keys(self.password)
        mydriver.find_element_by_name("submit").click()
        
        mydriver.get("https://get.cbord.com/gwu/full/funds_home.php")
        html = mydriver.page_source
        soup = BeautifulSoup(html, "lxml")

        mydriver.close()

        return soup
        

    def htmlToDataFrame(self):

        soup = self.loginToAccount()

        table = soup.find(
            "table", {"class": "table table-striped table-bordered"})

        # adds all table rows
        rows = list()
        for row in table.findAll("tr"):
            rows.append(row)

        print("Extracting spending history...")

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

        print("Saving to csv file...")

        myfile = '%s' % (self.login.strip('@gwmail.gwu.edu')) + '_gworld_dollars.csv'
        df.to_csv(myfile)

        return myfile

    def analysis(self):

        print("Reading information...")
        df = pd.read_csv('%s' % (self.login.strip('@gwmail.gwu.edu')) + '_gworld_dollars.csv',
                         parse_dates=['Date'])
        df = df.sort_values(by='Date')
        df.set_index('Date', inplace=True)

        df1 = df.truncate(before='2018-01-06')
        df1['CurrentVal'] = 0
        # df1['Current Value'] = df1['Price'] - df1['Current Value']
        df1.CurrentVal = 1350 * 2 - df1.Price.cumsum()

        df1.rename(columns={'Unnamed: 0': 'Count'}, inplace=True)
        del df1['Count']

        plt.figure()

        x = df1.index
        y = df1['CurrentVal']

        print("Plotting and calculating stats...")

        plt.plot(x, y, 'ko')

        df1.index = pd.to_datetime(df1.index)
        df1.index = df1.index.map(dt.datetime.toordinal)

        x1 = df1.index
        m, b = np.polyfit(x1, y, 1)

        plt.plot(x1, m * x1 + b, '-')

        predicted_date = int(-b / m)
        predicted_date = dt.datetime.fromordinal(predicted_date).date()
        print("Predicted to run out: " + str(predicted_date))

        print("Spending on average per day: $" + str(round(abs(m), 2)))

        plt.ylim(ymin=0)
        plt.xticks(rotation='vertical')
        plt.xlabel('Date')
        plt.ylabel('CurrentVal')

        plt.savefig('%s' % (self.login.strip('@gwmail.gwu.edu')) + '_spending.png', bbox_inches='tight')
        # plt.show()
        return str(predicted_date)

    def categoricalData(self):

        df = pd.read_csv('%s' % (self.login) + '_gworld_dollars.csv',
                         parse_dates=['Date'])

        df.rename(columns={'Unnamed: 0': 'Count'}, inplace=True)
        del df['Count']

        # df = df.groupby([''])
        # print(df.head())


# myobj = DiningDollars(myuser, mypass)
# myobj.htmlToDataFrame()
# myobj.analysis()
# myobj.categoricalData()

# TODO: figure out statistics on vendor information, places i buy the most, group by category

# df = pd.read_csv('suraj98_gworld_dollars.csv')
# df.rename(columns={'Unnamed: 0': 'Count'}, inplace=True)
# del df['Count']
# 
# df = df.sort_values(by='Date')
# 
# df = df[(df['Date'] >= '2018-01-06')]
# 
# df1 = df.groupby(['Date', 'Vendor']).count()['Price']
# 
# print(df1)









