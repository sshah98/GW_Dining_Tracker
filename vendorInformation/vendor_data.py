from urllib.request import urlopen
from bs4 import BeautifulSoup
from openpyxl import load_workbook

import pandas as pd

# simple code to scrape the dining website for the websites of all the vendors
def get_urls():
        
    from bs4 import BeautifulSoup
    import urllib.request

    resp = urllib.request.urlopen("https://dining.gwu.edu/where-eat")
    soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().get_param('charset'))

    mylist = []

    for link in soup.find_all('a', href=True):
        mylist.append(link['href'])

    df = pd.DataFrame({'test_set': mylist})
    writer = pd.ExcelWriter('output.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()

