import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from make_train_target import training_target
import pickle
import os

def data_pipeline():
    """
    fix march 2004

    convert int dates to datetimes!
    convert string dates to datetimes

    lowercase columns, make address column
    filter out "filed" permits


    """
    data = []
    for i, path in enumerate(os.listdir('data')):
        #I downloaded all the data into files with filename length 12/11. This'll filter out the other stuff.
        if len(path) > 12 or len(path) < 11:
            continue
        try:
            df = pd.read_excel('data/' + path)
        except:
            print(i)
            break
        df.columns = [str.lower(col) for col in df.columns]
        df.columns = df.columns.map(column_name_map)

        try:
            if len(df.columns) == 34:
                df['description'] = df['description'].astype(str) + df['unnamed: 33'].astype(str)
                df = df.drop(['unnamed: 33'], axis = 1)
            if len(df.columns) == 35:
                df['description'] = df['description'].astype(str) + df['unnamed: 33'].astype(str) + df['unnamed: 34'].astype(str)
                df = df.drop(['unnamed: 33', 'unnamed: 34'], axis = 1)
            if len(df.columns) == 42:
                df['description'] = df['description'].astype(str) + df['unnamed: 41'].astype(str)
                df = df.drop(['unnamed: 41'], axis = 1)
            if len(df.columns) == 43:
                df['description'] = df['description'].astype(str) + df['unnamed: 41'].astype(str) + df['unnamed: 42'].astype(str)
                df = df.drop(['unnamed: 41', 'unnamed: 42'], axis = 1)
        except KeyError as e:
            print(path)
            print(e)
            print(i)
            break
        data.append(df)

    #7 is march 2004
    mar_2004_cols = list(data[7].columns)
    mar_2004_cols = mar_2004_cols[:10] + mar_2004_cols[11:]  + [mar_2004_cols[10]]
    #74, 124 have those ints in the date column
    date_cols = ['status_date', 'file_date', 'expiration_date']
    for col in date_cols:
        data[74][col] = data[74][col].apply(int_to_date)
        data[124][col] = data[124][col].apply(int_to_date)

    predictor = pd.concat(data)

    predictor = predictor[predictor['status'] == 'ISSUED']

    for col in date_cols:
        predictor[col] = pd.to_datetime(predictor[col])

    predictor['street_number'] = predictor['street_number'].fillna(0).astype(int).astype(str)
    predictor['address'] = predictor[['street_number', 'avs_street_name']].apply(lambda x: ' '.join(x.astype(str)),axis = 1)
    predictor = predictor[~predictor['avs_street_name'].isnull()]
    return predictor

def target_pipeline(fires_df):
    """
    filter out non fires
    filter out non-addresses
    filter out single number addresses - these cannot be associated with buildings
    """
    fires_df = fires_df[fires_df['Primary Situation'].apply(lambda x: x[0] == '1')]
    fires_df = fires_df[fires_df['Address'].fillna('').apply(lambda x: len(x) > 0)]
    fires_df = fires_df[['Address', 'Incident Date']]
    fires_df.columns = ['address', 'date']
    fires_df['address'] = fires_df['address'].apply(str.upper)
    fires_df = fires_df.reset_index().drop('index', axis = 1)
    return fires_df

def fires_dl():
    """
    download fire incident data to data/Fire_Incidents.csv
    """
    with open('data/Fire_Incidents.csv', 'w') as file:
        r = requests.get('https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD')
        file.write(r.content)

def csv_dl(links, start):
    """
    download all building permit data, put them in individual csv's in data/
    """
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

def download():
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

    fires_dl()
