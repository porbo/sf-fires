

def coloring(number):
    if number > .7:
        return 'r'
    elif number > .4:
        return 'orange'
    else:
        return 'g'
f = np.vectorize(coloring)

def plot_predictions(pred):
    """
    plot predictions of fire risk, color coded and placed where the actual building is.
    Also plot actual buildings where fires happened.

    Save results to results/pred_actual.png
    """
    f = np.vectorize(coloring)

    with open('train/test_mask.p', 'rb') as file:
        mask = pickle.load(file)

    y = (pred['fire_rate_after'] > 0).astype(int).values

    sample_idx = np.random.choice(mask.sum(), 1000)

    x_axis, y_axis = np.array([x for x,y in pred.location]), np.array([y for x,y in pred.location])

    fig, axs = plt.subplots(1,2, figsize = (15,5))
    axs[0].set_title('predicted fire risk. red = high, orange = med, green = low')
    axs[0].set_xlabel('longitude')
    axs[0].set_ylabel('latitude')
    axs[0].scatter(x_axis[mask][sample_idx], y_axis[mask][sample_idx], c = f(pred['prediction'][mask].iloc[sample_idx]), alpha = .5, s = 20)

    axs[1].set_title('actual fires')
    axs[1].set_xlabel('longitude')
    axs[1].set_ylabel('latitude')
    axs[1].scatter(x_axis[mask][sample_idx], y_axis[mask][sample_idx], c = f(y[mask][sample_idx]), alpha = .5, s = 20)

    fig.savefig('')
