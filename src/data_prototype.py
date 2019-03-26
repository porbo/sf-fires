import pandas as pd
from pandas import ExcelFile
import os

fires = pd.read_csv('data/Fire_Incidents.csv')
"""
for now, just look at address and date
saved it to a csv
"""
# target = fires[['Incident Date', 'Address']]
# target['date'] = pd.to_datetime(target['Incident Date'])
# target = target.set_index('date')
# target = target.drop('Incident Date', axis = 1)
# target = target.dropna()
# target.to_csv('data/target.csv')

target = pd.read_csv('data/target.csv')

data = []

def change_permit_df(df):
    #take the dataframe of permit filings
    #return a dataframe of approved filings with:
    df.columns = [str.lower(col) for col in df.columns]
    cols = ['file_date', 'estimated cost', 'proposed use', 'proposed units', 'proposed stories', 'street_number', 'avs_street_name', 'avs_street_sfx', 'description']
    df = df[cols]
    df['address'] = df[['street_number', 'avs_street_name', 'avs_street_sfx']].apply(lambda x: ' '.join(x.astype(str)),axis = 1)

    df = df.drop(['street_number', 'avs_street_name', 'avs_street_sfx'], axis = 1).set_index('file_date')
    return df

for path in os.listdir('data'):
    #I downloaded all the data into files with filename length 12. This'll filter out the other stuff.
    if len(path) != 12:
        continue

    df = pd.read_excel('data/' + path)
    data.append(df)
    #data.append(change_permit_df(df))

predictor = pd.concat(data)
predictor.to_csv('data/predictor.csv')

#On second thought, I'll drop this file. There's just no need for it when I'm saving my results to csv files.
