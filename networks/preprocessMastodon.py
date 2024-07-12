


import gzip
import ujson
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from tqdm.auto import tqdm
import re

dataPath = Path('/mnt/cnets/datasets/mastodon/archives/')
outputPath = Path('Data')
datasetName = "debate2024_Jun"
dateRangeStart = "2024-06-25"
dateRangeEnd = "2024-07-02"

searchTerms = ["biden", "debate", "trump"]

# create regex for finding any of the search terms no case sensitive
searchRegex = re.compile("|".join(searchTerms), re.IGNORECASE)


#dataPath/YYYY-MM/YYYY-MM-DD/*json.gz
dateRange = pd.date_range(start=dateRangeStart, end=dateRangeEnd, freq='D')
dateRange = [str(date.date()) for date in dateRange]
allData = []
for date in dateRange:
    datePath = dataPath / date[:7] / date
    print(datePath)
    filenames = list(datePath.glob('*.json.gz'))
    for file in tqdm(filenames):
        with gzip.open(file, 'rt', encoding="utf-8") as f:
            for line in f:
                # if the line contains any of the search terms
                if searchRegex.search(line) is None:
                    continue
                entry = ujson.loads(line)
                allData.append(entry)


df = pd.DataFrame(allData)
# save the data to pickle and feather
df.to_pickle(outputPath / f"{datasetName}.pkl")
# column account is a dictionary, flatten it and add prefix account_ to all its columns
account = pd.json_normalize(df['account'])
account.columns = ['account_' + col for col in account.columns]
df = pd.concat([df, account], axis=1)
df.drop(columns=['account'], inplace=True)
# convert account_fields to json
df['account_fields'] = df['account_fields'].apply(lambda x: ujson.dumps(x))
df.to_feather(outputPath / f"{datasetName}.feather")


# count/frequency for event_type column
countFrequency = df['event_type'].value_counts()


# content uses html tags, such as p and a, parse
