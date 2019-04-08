# San Francisco Fire Risk

## Summary
Cities are complicated. But perhaps we could get a decent picture by looking at how a city has changed - namely, by looking at the building modification permits that have been issued.

This project tries to use information from those permits to predict fire risk at addresses in San Francisco. 

## Data
Much of the information in these permits can be found in the descriptions. Most machine learning algorithms require numerical vectors as input, so I converted the descriptions using Tfidf - term frequency inverse document frequency. That is, each description was converted to a numerical vector where each element is the frequency of a word in the description, weighted by how rare the word is within all the descriptions. 

Word frequency is used over word counts to control for the fact that descriptions have different lengths, and the rarity scaling is meant to put priority on rare words which are more likely to differentiate descriptiosn. It's hard to conclude anything from a descrpition having the word "the", but words like "food" and "beverage" are strong indicators that the building may be a restaurant.

## Findings
Using those vectorized descriptions, I constructed a logistic regression model to predict whether or not a fire will happen at a building.

Logistic regression was chosen for two reasons: fitting speed and interpretability. 

The fitting speed allowed rapid iteration through ideas.

And with logistic regression, when the features have the same scale, we can look at the magnitude of coefficients as an indication of how helpful that word's prescence is in predicting fire risk. 

Below is a chart of words, and the percentage of permits containing that word after which a fire occurred.

| Word	| Fire Risk
|:------|:--------
| bart 	| 0.8118
| mall 	| 0.1865
| kiosk 	| 0.5946
| hospital 	| 0.44
| laminate 	| 0.2715

For reference, the overall "Fire Risk" was about 13%. 

As we can see, some words indicated a much higher fire risk. In general, the model seems to be good at finding places with lots of people (indicated by words like mall, hospital, bart) - after all, more people means more chance that something goes wrong.

### Model performance

With this model, the ROC-AUC score was 0.812

This can be interpreted as "the chance a random positive case has a higher fire risk rating than a random negative case"


Here is a plot of predictions, on top of a map of San Francisco. Each point represents a permit, and the color represents the predicted likelihood that a fire will occur at that location after the permit is issued.


![Predicted fire risk](results/predictions.png)

And for reference, here is a plot of those same locations with color representing whether a fire actually happened there.

![Fires](results/actual.png)

The model was trained using permits and fires occuring before 2015. The plots were made using a random sample of permits issued in 2015, and fires occuring up until February 2019. 

The separation of train and test data is standard to give a more accurate idea of how well the model makes true predictions about the future. The test set was chosen a few years ago so we can more accurately gauge fire risk - if we tested using permits issued in 2019, for instance, there is simply not enough time to see if a fire happened afterward.


### Exploring increases in fire risk over time

I also tried to see if there were perhaps building modifications that cause an increase in fire risk. 

This was done by using the same model, but switching the target from "was there a fire here afterward?" to "did fires per year increase after the permit was issued?"

Below is a table of the words with highest coefficient in that model, along with counts of permits where the fires per year increased, stayed the same, and decreased.

"general" refers to the total counts, without filtering for any words.

|Word       | 	increase 	|same 	|decrease 
|:-----------|:--------|:----------|:---------
|maher 	|17946 	|18404 	|1464 	
|traps 	|454 	|95 	|8 	
|apt 	|3152 	|6321 	|759 	
|ref 	|12313 	|18399 	|1950 	
|deferred 	|441 	|655 	|69 	
|mep 	|3201 	|2616 	|614 	
|ordinance 	|5046 	|6602 	|610 	
|exh 	|1113 	|1421 	|326 	
|general 	|66271 	|313753 	|43075 	

Notes:

Maher refers to the Maher Ordinance, and is generally mentioned to say something like "compliance with the maher ordinance is not necessary".

Traps refers to p-traps, which are placed under sinks to trap waste water.

ref indicates a reference to another permit.

MEP stands for Mechanical, Electrical, Plumbing

One thing to note is that many of these words could help indicate the age of the building. For example, replacing p-traps is a sign that the building is old enough for them to wear out. This is interesting since building age is not readily available information.

## Other
Building modification descriptions can be grouped into topics.

Using NMF, we can get representative words for any number of automatically created topics. In this case, 6 topics seemed to cover a variety of building modification types, without creating redundant or nonsensical topics.

|Topic   |  Words                                                                | Fire risk
|:-------|:----------------------------------------------------------------------|:-----------
|1       | family, dwelling, reroofing, roofing, renew, report                   | .0286
|2       | replace, new, kitchen, remodel, window, bathroom                      | .0614
|3       | apartment, reroofing, soft, appendix, unit, chapter, retrofit, story, | .1363
|4       | office, ref, floor, fire, sprinkler, relocate, alarm                  | .3572
|5       | work, final, inspection, obtain, approved, complete, under, all       | .1146
|6       | food, beverage, hndling, retail, sale, fire, sign, system, new        | .2175

In this table, the fire risk is the proportion of permits classified under a given topic where a fire happened at that address after the permit was issued.

The lowest fire risks were in topics 1 and 2. Based on the representative words, these are permits for homes for single families. Compared to other topics, these buildings likely have far fewer people, and thus fewer chances for someone to make a mistake.

## Future
Early data exploration indicated that the height of a building was quite helpful in predicting fire risk. Unfortunately, this was not available in my training data from before 2015. If this project were to be repeated in the future, better predictions could be attained using that data.


Target: Fire incidents in San Francisco
https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric
    Predictors: Building permit filings
https://sfdbi.org/building-permits-filed-and-issued

Code to download the building permit filings is at https://github.com/porbo/sf-fires/src/download_data.py

US Census Bureau api for geocoding: https://www.census.gov/geo/maps-data/data/geocoder.html

citing sklearn
https://scikit-learn.org/stable/about.html#citing-scikit-learn

citing nltk
https://groups.google.com/forum/#!topic/nltk-users/CS2fCFxvu1I

https://help.plot.ly/citations/

https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc
