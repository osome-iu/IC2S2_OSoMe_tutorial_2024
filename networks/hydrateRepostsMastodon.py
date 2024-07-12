


import gzip
import ujson
import pandas as pd
import numpy as np
from pathlib import Path
import datetime
from tqdm.auto import tqdm
import re
import mastodon.errors as mastodonErrors
from mastodon import Mastodon
import mastodon as mastodonLib
# import sleep
import time


access_token="CleVf2DFvXbm_dJaRHnTgfylO6lZUxB09AGL6jhLnPg"

inputPath = Path('Data')
datasetName = "debate2024_Jun_mastodon"

df = pd.read_feather(inputPath / f"{datasetName}.feather")
df["base_url"] = df["url"].apply(lambda x: "/".join(x.split("/")[:3]))
df["status_id"] = df["uri"].apply(lambda x: x.split("/")[-1])
api_base_url = 'https://mastodon.social'

allUsers = set(df["account_uri"].unique())
allReblogs = {}
problematicIDs = []

baseURLsTQDM = tqdm(list(df["base_url"].value_counts().items()), desc="Base URLs")
for api_base_url, _ in baseURLsTQDM:
    baseURLsTQDM.desc = api_base_url
    mastodon = Mastodon(api_base_url=api_base_url)
    dfReblogged = df[df.reblogs_count>0]
    dfRebloggedOnlyBaseURL = dfReblogged[dfReblogged.base_url==api_base_url]

    def addReblogToID(statusID,reblog):
        # filter reblogs ids to be in allUsers
        reblogFiltered = [reblog for reblog in reblog if reblog["uri"] in allUsers]
        if(reblogFiltered):
            if statusID in allReblogs:
                allReblogs[statusID].append(reblogFiltered)
            else:
                allReblogs[statusID] = [reblogFiltered]

    blogTQDM = tqdm(dfRebloggedOnlyBaseURL["status_id"],leave=False,desc="Reblogs")
    for statusID in blogTQDM:
        success = False
        while not success:
            try:
                reblogs = mastodon.status_reblogged_by(statusID)
                success = True
                if(reblogs):
                    addReblogToID(statusID,reblogs)
                    blogTQDM.desc = f"Reblogs: {len(allReblogs)}"
            except mastodonErrors.MastodonRatelimitError:
                nextResetPOSIXTime = mastodon.ratelimit_reset
                # wait until the rate limit is reset
                timeDifference = nextResetPOSIXTime - time.time()
                print(f"\nRate limit reached. waiting {timeDifference} seconds...\n")
                if(timeDifference>0):
                    time.sleep(timeDifference)
                time.sleep(5)
            except mastodonErrors.MastodonNotFoundError:
                blogTQDM.desc = f"Reblogs: {len(allReblogs)} (problematicID: {statusID})"
                problematicIDs.append((api_base_url,statusID))
                reblogs = []
                success = True
                continue
            except Exception as anotherError:
                print(f"Another error occurred: {anotherError}")
                blogTQDM.desc = f"Reblogs: {len(allReblogs)} (problematicID: {statusID})"
                problematicIDs.append((api_base_url,statusID))
                reblogs = []
                success = True
                continue
        while(reblogs):
            try:
                reblogs = mastodon.fetch_next(reblogs)
            except mastodonErrors.MastodonRatelimitError:
                nextResetPOSIXTime = mastodon.ratelimit_reset
                # wait until the rate limit is reset
                timeDifference = nextResetPOSIXTime - time.time()
                print(f"Rate limit reached. waiting {timeDifference} seconds...")
                if(timeDifference>0):
                    time.sleep(timeDifference)
                time.sleep(5)
            except Exception as anotherError:
                print(f"Another error occurred: {anotherError}")
                blogTQDM.desc = f"Reblogs: {len(allReblogs)} (problematicID: {statusID})"
                problematicIDs.append((api_base_url,statusID))
                reblogs = []
                continue
            if(reblogs):
                addReblogToID(statusID,reblogs)
                blogTQDM.desc = f"Reblogs: {len(allReblogs)}"
            else:
                break

