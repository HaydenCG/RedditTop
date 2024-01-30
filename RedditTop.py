import requests 
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import praw
import nltk

from dotenv import load_dotenv
import os

load_dotenv()



CLIENT_ID = os.getenv('CLIENT_ID')
SECRET_KEY = os.getenv('SECRET_KEY')

#make keys

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

data = {
    'grant_type': 'password',
    'username': 'ALLPARSER',
    'password': 'CATSONMARS' 
}
#initizalize credentials

headers = {'User-Agent': "MyAPI/0.0.1"}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                   auth = auth, data = data, headers = headers)

TOKEN = res.json()['access_token']
headers['Authorization'] = f'bearer {TOKEN}'

print("--HEADERS--")
print(headers)
print("---------------" +"\n")

requests.get("https://oauth.reddit.com/api/v1/me", headers = headers).json() #make the request


sub = input(str("Input desired subreddit (lowercase)"+ "\n"))

res = requests.get('https://oauth.reddit.com/r/'+sub+'/hot', #initial checker
                  headers = headers)
res.json()

title_list = []
for post in res.json()['data']['children']:
    title_list.append(post['data']['title'])
    
title_list #check to make sure titles are in order
response_df = pd.DataFrame()

for post in res.json()['data']['children']:
    response_df = response_df._append({
        'subreddit' : post['data']['subreddit'],
        'title': post['data']['title']
    }, ignore_index = True)

print(response_df)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
print("\n" + "--TEST--TOP1--")
print(response_df['title'][0]) #checking to make sure i remember how grabbing data from dataframes works lmao
print("--END--TEST--TOP1--" + "\n")

sid = SentimentIntensityAnalyzer()

response_df['Score'] = 1

for i in range(len(response_df['title'])):
    temp_sentence = response_df['title'][i]
    scores = sid.polarity_scores(temp_sentence)
    response_df['Score'][i] = scores['compound']
    
print(response_df) #analyze the sentiment

sb.histplot(y = response_df['title'], x = response_df['Score'], bins = 100) #plot
plt.show()
