from sklearn.decomposition import NMF

def topics(n_components):
"""
Use NMF to find topics for the permit descriptions
Returns a 2d array, where rows are representative words of a topic, for each topic.
"""
    with open('models/vec.p', 'rb') as file:
        vec = pickle.load(file)

    with open('data/text.p', 'rb') as file:
        text = pickle.load(file)

    vocab_idx = {value:key for (key, value) in vec.vocabulary_.items()}

    X_text = vec.transform(text)

    nmf = NMF(n_components = n_components)
    nmf.fit(X_text)
    B = nmf.components_
    A = nmf.transform(X_text)
    word_clusters = np.array([[vocab_idx[idx] for idx in row][::-1] for row in B.argsort()[:,-11:]])

    with open('results/word_clusters.p', 'wb') as file:
        pickle.dump(word_clusters, file)

    return word_clusters
