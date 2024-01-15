import json
import os

import kopenai

kai = kopenai.KOpenAI()

with open('./prompts/functions/pandas_io.json') as f:
    pnf = json.load(f)
    prompt = pnf['prompt']
    functions = pnf['functions']

kai.chat(prompt, role='system')
# its unable to detect dates
kai.chat('Read the csv in /home/karthic/Desktop/Programming/data/house-prices-advanced-regression-techniques/train.csv with index Id', functions=functions)
# try explicitly specifying the date
# setup infra to call and structure weather response
# expand to multiple dates
# expand to multiple locations
# expand to multiple fields
