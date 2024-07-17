


import gzip
import ujson
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from tqdm.auto import tqdm
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Path to where the json files are stored
dataPath = Path('<path to the json files>')
outputPath = Path('Data')
datasetName = "dataset_mastodon"
# time range to be considered:
dateRangeStart = "2024-06-25"
dateRangeEnd = "2024-07-03"

# example of search terms you can fully customize the filter procedure
searchTerms = ["biden", "debate", "trump"]

# create regex for finding any of the search terms no case sensitive
searchRegex = re.compile("|".join(searchTerms), re.IGNORECASE)

# get URL list from text
def getURLs(text):
    return re.findall(r'(https?://[^\s]+)', text)

def extractText(html_snippet):
    soup = BeautifulSoup(html_snippet, 'html.parser')

    # Extract plain text but put a space when there is an a query or new line
    # also at the end of p
    for a in soup.find_all('a'):
        a.replace_with(f" {a.get_text()} ")
    for br in soup.find_all('br'):
        br.replace_with(" ")

    plain_text = soup.get_text()
    
    return plain_text

def clearURL(url):
    if(url):
        try:
            return urljoin(url, urlparse(url).path)
        except ValueError:
            pass
    return url

def extractURLs(html_snippet,server= None):
    soup = BeautifulSoup(html_snippet, 'html.parser')

    # Extract plain text
    plain_text = soup.get_text()

    # Extract links
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    # also get all URLs in the plain text
    links += getURLs(plain_text)
    links = [clearURL(url) for url in links]
    # clean all the urls
    # remove any urls that are formatted as https://server/* or http://server/* since they are internal links
    if(server):
        links = [url for url in links if url is not None and not url.startswith(f"https://{server}") and not url.startswith(f"http://{server}")]
    return list(set(links))


filenames = list(dataPath.glob('*.json'))
for file in tqdm(filenames):
    with open(file, 'rt', encoding="utf-8") as f:
        for line in f:
            # if the line contains any of the search terms
            if searchRegex.search(line) is None:
                continue
            entry = ujson.loads(line)
            allData.append(entry)

# set id, in_reply_to_id and in_reply_to_account_id to strings
for entry in allData:
    entry["id"] = str(entry["id"])
    if entry["in_reply_to_id"]:
        entry["in_reply_to_id"] = str(entry["in_reply_to_id"])
    if entry["in_reply_to_account_id"]:
        entry["in_reply_to_account_id"] = str(entry["in_reply_to_account_id"])

df = pd.DataFrame(allData)
# save the data to pickle and feather
df.to_pickle(outputPath / f"{datasetName}.pkl") 


df = pd.read_pickle(outputPath / f"{datasetName}.pkl")
# column account is a dictionary, flatten it and add prefix account_ to all its columns
account = pd.json_normalize(df['account'])
account.columns = ['account_' + col for col in account.columns]
df = pd.concat([df, account], axis=1)
df.drop(columns=['account'], inplace=True)
# convert account_fields to json
df['account_fields'] = df['account_fields'].apply(lambda x: ujson.dumps(x))



# content uses html tags, such as p and a, parse
dfOutput = pd.DataFrame()
dfOutput["creation_date"] = pd.to_datetime(df['created_at'],format="mixed",utc=True)
dfOutput["text"] = df["content"].map(extractText)
# replace \n with space and remove extra spaces
dfOutput["text"] = dfOutput["text"].str.replace("\n", " ").str.replace(" +", " ")
# get mastodon server from post_id
df["server"] = df["uri"].str.extract(r"https://([^/]+)")[0]
dfOutput["data_server"] = df["server"]
dfOutput["hashtags"] = dfOutput["text"].str.lower().str.findall(r"#\w+")
dfOutput["hashtags"] = dfOutput["hashtags"].map(lambda x: x if x == x and x is not None else [])
dfOutput["mentioned_users"] = dfOutput["text"].str.lower().str.findall(r"@\w+")
dfOutput["mentioned_users"] = dfOutput["mentioned_users"].map(lambda x: x if x == x and x is not None else [])
dfOutput["urls"] = df[["content","server"]].apply(lambda content_server: extractURLs(*content_server), axis=1)
dfOutput["urls"] = dfOutput["urls"].map(lambda x: x if x == x and x is not None else [])
dfOutput["post_id"] = df["uri"]
# when account_uri is not available use account_url instead
dfOutput["user_id"] = df["account_uri"].combine_first(df["account_url"])

dfOutput["linked_post"] = df["in_reply_to_id"]
dfOutput["linked_post_user_id"] = df["in_reply_to_account_id"]
# no root post for Mastodon
dfOutput["root_post"] = dfOutput["linked_post"]
dfOutput["root_post_user_id"] = dfOutput["linked_post_user_id"]

# if has root or linked, set post_type to reply otherwise post
dfOutput["post_type"] = "post"
dfOutput.loc[dfOutput["linked_post"].notnull() | dfOutput["root_post"].notnull(), "post_type"] = "reply"
# Extra data has prefix data_
dfOutput["data_langs"] = df["language"]
dfOutput["data_internal_id"] = df["id"].astype(str)
dfOutput["data_internal_user_id"] = df["account_id"].astype(str)
dfOutput["data_internal_id"] = df["id"].astype(str)
dfOutput["data_account_followers_count"] = df["account_followers_count"]
dfOutput["data_account_following_count"] = df["account_following_count"]
dfOutput["data_account_bot"] = df["account_bot"]

dfOutput.drop_duplicates(subset=["post_id"], keep='last', inplace=True)

# Making sure the data is in the date range
dfFiltered = dfOutput[dfOutput['creation_date'].between(dateRangeStart, dateRangeEnd)]


with gzip.open(outputPath / f"{datasetName}.feather.gz", 'wb') as f:
    dfFiltered.to_feather(f)
