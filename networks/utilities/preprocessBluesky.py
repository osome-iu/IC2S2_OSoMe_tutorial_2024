import gzip
import ujson
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from tqdm.auto import tqdm
import re
import unalix
import gzip
import csv

# Path to where the json files are stored
dataPath = Path('osome-bluesky-streamer/')
outputPath = Path('Data')
datasetName = "dataset_bluesky"

# time range to be considered:
dateRangeStart = "2024-06-25"
dateRangeEnd = "2024-07-03"

# example of search terms you can fully customize the filter procedure
searchTerms = ["biden", "debate", "trump"]

# create regex for finding any of the search terms no case sensitive
searchRegex = re.compile("|".join(searchTerms), re.IGNORECASE)


allData = []
reposts = []
actions = set()
filenames = list(dataPath.glob('*.json'))
for file in tqdm(filenames):
    with open(file, 'rt', encoding="utf-8") as f:
        for line in f:
            # if the line contains any of the search terms
            entry = ujson.loads(line)
            if entry["action"] !="create":
                actions.add(entry["action"])
                continue
            if entry["type"] == "app.bsky.feed.repost":
                # and if subject is not a int
                if("subject" in entry and entry["subject"] and isinstance(entry["subject"], dict)):
                    repostURI = entry["uri"]
                    repostCID = entry["cid"]
                    originalURI = entry["subject"].get("uri", None)
                    originalCID = entry["subject"].get("cid", None)
                    createdAt = entry["createdAt"]
                    reposts.append((repostURI, repostCID, originalURI, originalCID, createdAt))
            elif entry["type"] == "app.bsky.feed.post":
                if searchRegex.search(line) is None:
                    continue
                allData.append(entry)



df = pd.DataFrame.from_dict(allData)
# save the data to pickle and feather
df.to_pickle(outputPath / f"{datasetName}.pkl")
dfReposts = pd.DataFrame(reposts, columns=["repost_uri", "repost_cid", "original_uri", "original_cid", "createdAt"])
df.to_pickle(outputPath / f"{datasetName}_reposts.pkl")


def getAuthorFromURI(uri):
    # at://did:plc:ghx4g5bwoazaeoq3c3nf7tl2/app.bsky... -> did:plc:ghx4g5bwoazaeoq3c3nf7tl2
    if(isinstance(uri, str)):
        return uri.split("/")[2]
    else:
        return pd.NA

# get URL list from text
def getURLs(text):
    return re.findall(r'(https?://[^\s]+)', text)


dfOutput = pd.DataFrame()
dfOutput["creation_date"] = pd.to_datetime(df['createdAt'],format="mixed",utc=True)
dfOutput["hashtags"] = df["text"].str.lower().str.findall(r"#\w+")
dfOutput["hashtags"] = dfOutput["hashtags"].map(lambda x: x if x == x and x is not None else [])
dfOutput["mentioned_users"] = df["text"].str.lower().str.findall(r"@\w+")
dfOutput["mentioned_users"] = dfOutput["mentioned_users"].map(lambda x: x if x == x and x is not None else [])
dfOutput["urls"] = df["text"].map(getURLs)
dfOutput["urls"] = dfOutput["urls"].map(lambda x: x if x == x and x is not None else [])
dfOutput["text"] = df["text"]
# replace \n with space and remove extra spaces
dfOutput["text"] = dfOutput["text"].str.replace("\n", " ").str.replace(" +", " ")
dfOutput["user_id"] = df["author"]
dfOutput["post_id"] = df["uri"]
dfReplies = pd.json_normalize(df['reply'])
dfOutput["linked_post"] = dfReplies["parent.uri"]
dfOutput["linked_post_user_id"] = dfReplies["parent.uri"].map(getAuthorFromURI)
dfOutput["root_post"] = dfReplies["root.uri"]
dfOutput["root_post_user_id"] = dfReplies["root.uri"].map(getAuthorFromURI)
# if has root or linked, set post_type to reply otherwise post
dfOutput["post_type"] = "post"
dfOutput.loc[dfOutput["linked_post"].notnull() | dfOutput["root_post"].notnull(), "post_type"] = "reply"
dfOutput["data_langs"] = df["langs"].map(lambda x: ";".join(x) if x == x and x is not None else None)
dfOutput = dfOutput[dfOutput['creation_date'].between(dateRangeStart, dateRangeEnd)]

# Only reposts of posts in the dataset will be considered.
uri2Index = {uri: i for i, uri in enumerate(dfOutput["post_id"])}
dfReposts["repost_index"] = dfReposts["original_uri"].apply(lambda x: uri2Index.get(str(x), -1))
dfRepostsFiltered = dfReposts[dfReposts["repost_index"]>=0].reset_index(drop=True)
# using the repost_index, I want to create a new dataFrame with all the data from dfOutput but changing
# the user_id to the user_id of the repost and the post_id to the repost_id
# the original_url should move to a new column called linked_post and the original_user_id to linked_post_user_id
# also post_type should be changed to repost
dfRepostsHydrated = dfOutput.iloc[dfRepostsFiltered["repost_index"]].copy().reset_index(drop=True)

dfRepostsHydrated["creation_date"] = pd.to_datetime(dfRepostsFiltered['createdAt'],format="mixed",utc=True)
dfRepostsHydrated["user_id"] = dfRepostsFiltered["repost_uri"].map(getAuthorFromURI)
dfRepostsHydrated["post_id"] = dfRepostsFiltered["repost_uri"]
dfRepostsHydrated["post_type"] = "repost"
dfRepostsHydrated["linked_post"] = dfRepostsFiltered["original_uri"]
dfRepostsHydrated["linked_post_user_id"] = dfRepostsFiltered["original_uri"].map(getAuthorFromURI)

dfOutputWithReposts = pd.concat([dfOutput, dfRepostsHydrated], ignore_index=True)

dfOutputWithReposts.drop_duplicates(subset=["post_id"], keep='last', inplace=True)
dfFiltered = dfOutputWithReposts[dfOutputWithReposts['creation_date'].between(dateRangeStart, dateRangeEnd)]

with gzip.open(outputPath / f"{datasetName}.feather.gz", 'wb') as f:
    dfFiltered.to_feather(f)
