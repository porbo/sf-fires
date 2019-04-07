import time
import requests
import pickle

get_locations(addresses):
    start_time = time.clock()
    locations = {}
    for i, address in enumerate(addresses):
        r = requests.get('https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=' + address + ' San Francisco CA&benchmark=9&format=json')
        try:
            locations[address] = tuple(r.json()['result']['addressMatches'][0]['coordinates'].values())
        except:
            print(i, address)
            locations[address] = (None, None)
        if i % 500 == 0:
            print('Locations retrieved:', i, '  Elapsed time: ', time.clock() - start_time)


    with open('data/locations.p', 'wb') as file:
        pickle.dump(locations, file)
