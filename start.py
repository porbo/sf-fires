"""
arguments:
    extracttext:        get an array of descriptions out of the predictor dataframe, and store as data/text.p. Without this, just load text.p
    buildvectorizer:    build a TfidfVectorizer from the array of descriptions. Otherwise, load models/vec.p
    buildmodels:        fit the models and save pickles as models/model_up.p and models/model.p. The former predicts if fire rate will increase, the latter predicts if there will be fires afterward. (otherwise load the previously built models)

"""

from src.logit_gb import LogitGB
from src.topics import topics
from src.plotting import plot_predictions
import pickle
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter

if __name__ == '__main__':
    #let's make the text and stuff:
    with open('data/predictor.p', 'rb') as file:
        predictor = pickle.load(predictor)

    train_mask = predictor['status_date'].apply(lambda x: x.year < 2015).values
    test_mask = predictor['status_date'].apply(lambda x: x.year < 2016).values
    test_mask = test_mask & ~train_mask

    with open('train/test_mask.p', 'wb') as file:
        pickle.dump(test_mask, file)

    if 'extracttext' in sys.argv:
        text = predictor[['existing_use', 'proposed_use', 'description']].apply(lambda x: ' '.join(x), axis = 1).values
        with open('data/text.p', 'wb') as file:
            pickle.dump(text, file)
    else:
        with open('data/text.p', 'rb') as file:
            text = pickle.load(file)

    #built the vectorizer based on train data if specified, otherwise take the existing vectorizer
    if 'buildvectorizer' in sys.argv:
        vec = TfidfVectorizer()
        vec.fit(text[train_mask])
        with open('models/vec.p', 'wb') as file:
            pickle.dump(vec, file)
    else:
        with open('models/vec.p', 'rb') as file:
            vec = pickle.load(file)


    X_text = vec.transform(text)

    with open('data/fires_train.p', 'rb') as file:
        fires_train = pickle.load(file)

    pred_train = predictor.iloc[train]
    pred_train['fires_before'] = fires[:,0]
    pred_train['fires_after'] = fires[:,1]
    pred_train['fire_rate_before'] = 365*pred_train['fires_before']/(pred_train['status_date'] - pd.to_datetime('2003-01-01')).apply(lambda x: x.days)
    pred_train['fire_rate_after'] = 365*pred_train['fires_after']/(pd.to_datetime('2014-12-31') - pred_train['status_date']).apply(lambda x: x.days)

    if 'buildmodels' in sys.argv:
        model_up = LogitGB()
        model_up.fit(X_text[train_mask], pred_train, pred_train)

        model = LogitGB()
        model.fit(X_text[train_mask], pred_train, pred_train, any = True)

        with open('models/model_up.p', 'wb') as file:
            pickle.dump(model_up, file)
        with open('models/model.p', 'wb') as file:
            pickle.dump(model, file)
    else:
        with open('models/model_up.p', 'rb') as file:
            model_up = pickle.load(file)
        with open('models/model.p', 'rb') as file:
            model = pickle.load(file)


    #print out a 2d array. each row is a topic for permits, shown as representative words.
    topics = topics(6)
    print('Topics of descriptions:')
    print(topics)

    predictor['fires_before'] = fires[:,0]
    predictor['fires_after'] = fires[:,1]
    predictor['fire_rate_before'] = 365*predictor['fires_before']/(predictor['status_date'] - pd.to_datetime('2003-01-01')).apply(lambda x: x.days)
    predictor['fire_rate_after'] = 365*predictor['fires_after']/(pd.to_datetime('2014-12-31') - predictor['status_date']).apply(lambda x: x.days)

    with open('data/locations.p', 'rb') as file:
        locations = pickle.load(file)
    predictor['location'] = predictor['address'].apply(lambda x: locations[x])

    #make plots of predicted fire risk and of actual fires happening, and save to file
    plot_predictions(predictor)

    #get important words in the model based on logistic regression coefficients
    words = Counter()
    for word, idx in vec.vocabulary_.items():
        words[word] = model.m1.coef_[0][idx]
    print('Most useful word in predicting fire risk: ', words.most_common(20))

    words_up = Counter()
    for word, idx in vec.vocabulary_.items():
        words_up[word] = model_up.m1.coef_[0][idx]
    print('Most useful word in predicting increases in fire rate: ', words.most_common(20))
