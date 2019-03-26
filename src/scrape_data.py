import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def csv_dl(links, start):
    for link in links:
        if link.string[:3] == 'Jan':
            start -= 1
        path = base + link['href']
        #2 types of links: a short one that leads to a page with the dl (else statemtent), and direct links to the file
        if len(link['href']) > 11:
            pass
        else:
            s2 = BeautifulSoup(requests.get(path).content)
            path = s2.find('a', {'href': re.compile(r'/files*')})['href']

        resp = requests.get(path)
        with open('data/' + str(start) + link.string[:3] + '.xlsx', 'wb') as file:
            file.write(resp.content)
    return start

if __name__ == '__main__':
    base = "https://sfdbi.org"
    recent = "/building-permits-filed-and-issued"
    archive  = "/building-permits-filed-and-issued-archive"
    response = requests.get(base+recent)

    soup = BeautifulSoup(response.content)
    links_newer = soup.find_all('a', {'href':re.compile(r'/files*')})

    r2 = requests.get(base + archive)
    links_archive = BeautifulSoup(response.content).find_all('a', {'href':re.compile(r'/files*')})

    start = 2020
    start = csv_dl(links_newer, start)
    start = csv_dl(links_archive, start)
