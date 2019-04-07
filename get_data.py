"""
Download and preprocess data.
Afterward, in the data/ folder, we should have the following pickle files:
    predictor.p:    all the predictor data
    target.p:       target data
    fires_train.p:  the number of fires before and after each building permit is issued, using only data from before 2015
    fires.p:        same as above, using all available data.
    locations.p:    dictionary of addresses to longitude/latitude
"""
from src.download_data import download, data_pipeline, target_pipeline
from src.training_util import make_target_date_index, make
from src.make_train_target import make_train_target
from src.locations import get_locations
import pickle
import sys

if __name__ == '__main__':
    download()

    #basic data processing
    fires_df = pd.read_csv('data/Fire_Incidents.csv')

    #filter to only fires, by checking the first digit of the fire department's situation code.
    target = target_pipeline(fires_df)

    predictor = data_pipeline()
    with open('data/predictor.p', 'wb') as file:
        pickle.dump(predictor, file)

    #some caching for faster access to fires before/after a certain date
    target_date_index = {}
    for i, date in enumerate(target['date']):
        target_date_index[(date - start_date).days] = i
    with open('util/target_date_index.p', 'wb') as file:
        pickle.dump(target_date_index, file)

    #geocoding
    if 'loc' in sys.argv:
        get_locations(predictor['address'].unique())

    #construct target columns
    if 'maketarget' in sys.argv:
        train_mask = predictor['status_date'].apply(lambda x: x.year < 2015).values
        make_train_target(predictor[train_mask][['status_date', 'address']], target[train_mask])
        make_full_target(predictor[['status_date', 'address']], target)
