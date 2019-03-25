# sf-fires

San Francisco Fire Predictions
Description:
Predict fire incidents using information about buildings, from permit applications, with the goal of finding relationships between certain types of applications and fires. Alternatively, simply predict areas in the city more prone to fire. 
Presentation: 
 Slides, talking about predictive power of my model. Show off a map of current threat.
Next steps:
Look into other types of building related incidents, or alternatively, look for different predictors of fire.

Techniques:
    I have multiple csv’s: one for fire incidents, and one for each month of building permits. I’ll     need to combine rows from the different building permit datasets, and then link fire 
incidents to building permits by address. 

For address matching, it seems that a simple split will generally results in a group 
(address #, street name[, other words in the street name], street type abbreviation).
 If I lowercase things, and remove punctuation, matching should be pretty consistent.

Afterward, I’ll need to featurize descriptions of permits and fire incidents. I could start with tfidf or counts, and maybe look for other techniques later.

Potential Problems:
    There are quite a few factors to consider. 

    I’ll need to keep good track of dates, and account for permits filed after a fire; in these 
cases, the building changes obviously played no part in the fire. 

I’ll also need to consider how much time has passed since a permit was issued, in order 
to contextualize the significance of fire incidents that occur afterward. After all, a building 
that goes 10 years after a change without a fire is likely more significant than one that has 
no fires after a month. To start, I could choose a fixed time period after building permits to 
analyze, but I may consider more elegant solutions.

It may also be a challenge to split my data for validation. I believe the best solution for 
now would be to choose some addresses (and all associated fires) as a test set, though 
that could make it troublesome if I want to find effects of building changes on nearby buildings.

There is the possibility of illegal building changes without permits. Intuitively, these might be even more related to fires than legal changes. I will need to carefully consider what effects this might have on my results. 
Scope:
    To start, I plan to investigate the relation between descriptions of building permits issued 
and fire incidents in the same building. 

More specifically, I’ll start with predicting likelihood of fire within 5 years after a permit is 
issued, based on the description of the permit, existing and proposed use of the building, and numerical information like proposed and existing stories in the building.

By the end of the project, I plan to find a better way to express “likelihood” of a fire, accounting for multiple permits for the same building and details like frequency of fires, fires after 5 years, and more.

If time permits, I also plan to try and examine effects of building changes on fires near the building, rather than just fires in the same building. 
Resources:
    Planning to use sklearn, nltk, numpy, pandas. Possibly plotly, tensorflow if neural 
networks seem like a good idea.

Data is linked below.

Credits will be included.
    


Data:
Target: Fire incidents in San Francisco
https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric
    Predictors: Building permit filings
https://sfdbi.org/building-permits-filed-and-issued

Code to download the building permit filings is at https://github.com/porbo/sf-fires/src/download_data.py
