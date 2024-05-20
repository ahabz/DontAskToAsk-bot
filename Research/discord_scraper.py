import numpy
import os
import requests
import json
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

headers = {
        'Authorization': os.getenv("AUTHORIZATION", None)
    }

def getmessage(channelID):


    
    num = 0
    limit = 50
    filename = 'your-path/scrapedQ.csv'
    filename_iter = 'your-path/iterr.csv'

# Regex pattern to match questions seeking technical help
    regex_pattern = r'(?i)\b(question|questions|problems|problem|trying|familiar|who|which|here|Any|anyone|one|any|anybody|body|who|what|where|when|why|how|can|could|may|might|do|does|did|help|assist|guide|solve|troubleshoot|error|issue|problem|bug|fix)\b(?:\W+\w+){2,99}\?'

    if os.path.isfile(filename):  # if file exists, add to it

        beforeid = pd.read_csv(filename_iter)
        last_message_id = beforeid['id'].iloc[-1]
        print(last_message_id)
    else:

        last_message_id = None

    while True:

        query_parameters = f'limit={limit}'
        if last_message_id is not None:  # last id we got
           
            query_parameters += f'&before={last_message_id}' # add the id of the last message

        getRequest = requests.get(
            f'https://discord.com/api/v9/channels/{channelID}/messages?{query_parameters}', headers=headers)
        jsonObject = json.loads(getRequest.text)
        jsonToDf = pd.DataFrame(jsonObject)

        # conditions for scraping
        jsonIterrate = jsonToDf[['id', 'content']]

        # condition 01: only scraping ones with a question mark
        strQs = jsonIterrate[jsonIterrate['content'].str.contains(
            regex_pattern, regex=True)]
        strQs = strQs[['id', 'content']]

        if os.path.isfile(filename):  # if file exists, add to it

            scrapedDf = pd.read_csv(filename)

            print("====how many questions in batch:", len(strQs))

            print("====length of batch:", len(jsonIterrate))
            print("last message IDs OLD:", last_message_id)
            print("len scrapeddf   :", len(scrapedDf))

    # Print the first few rows of new messages
            combinedDf = pd.concat([scrapedDf, strQs], ignore_index=True)
            combinedDfIter = pd.concat(
                [scrapedDf, jsonIterrate], ignore_index=True)
            if not jsonIterrate.empty:
                last_message_id = jsonIterrate['id'].iloc[-1]
            # Your further processing with last_message_id
            else:
                print("DataFrame 'strq' is empty.")
            print("last message NEWW IDs NEWW:", last_message_id)

            num += 1
        else:
            combinedDf = pd.DataFrame(strQs)  # if not, make a new one
            combinedDfIter = pd.DataFrame(jsonIterrate)

        if not jsonIterrate.empty:
            last_message_id = jsonIterrate['id'].iloc[-1]
            # Your further processing with last_message_id
        else:
            print("DataFrame 'streq' is empty.", last_message_id)
            num += 1

        combinedDf.to_csv(filename, index=False)
        combinedDfIter.to_csv(filename_iter, index=False)
        if jsonIterrate.empty:
            print("emptyyyyyyy")
            break


getmessage('464539978442211330')
