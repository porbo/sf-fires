import time
import pickle
import pandas as pd
import numpy as np

if __name__ == '__main__':
    with open('train/target_date_index.p', 'rb') as file:
        target_date_index = pickle.load(file)
    with open('train/target_matching.p', 'rb') as file:
        target_matching = pickle.load(file)
    with open('train/fires_df.p', 'rb') as file:
        fires_df = pickle.load(file)

    fires = np.zeros((len(target_matching), 2))

    time1 = time.clock()
    for i, row in target_matching.iterrows():
        if i%10000 == 0:
            print('done with {} iterations'.format(i))
            print(time.clock() - time1)
        try:
            #part a
    #         p1 = time.clock()
            start = row['status_date']
            address = row['address']
            #part b
    #         p2 = time.clock()

            days = (start - start_date).days
            after = fires_df.iloc[:target_date_index[days]]
            before = fires_df.iloc[target_date_index[days]:]

            #part c
    #         p3 = time.clock()

            fires[i,0] = len(before[before['address'].apply(lambda x: address == x[:len(address)])])
            fires[i,1] = len(after[after['address'].apply(lambda x: address == x[:len(address)])])
    #         last = time.clock()

    #         a += p2 - p1
    #         b += p3 - p2
    #         c += last - p3
        except:
            print(i)
            print(sys.exc_info())
            break

    with open('train/fires.p', 'wb') as file:
        pickle.dump(fires, file)
