import numpy as np 
import json
import tweepy as tp 
from twitter import Twitter
import tw_cred as tc
from datetime import datetime
from datetime import timedelta
import pytz
import time
import pytz
import os


auth = tp.OAuthHandler(tc.API_KEY, tc.API_SECRET_KEY)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_SECRET_TOKEN)


api=tp.API(auth)


class Maujpur:

	def __init__(self,place):
		self.place = place

	def collect_tweets(self):
		tweets = []
		date1 = datetime(2020,2,1,0,0,0,0,pytz.UTC)
		date2 = datetime(2020,3,20,0,0,0,0,pytz.UTC)
		tc = 0
		for tweet in tp.Cursor(api.search,q = "Maujpur OR Tilak Nagar"+" -filter:retweets",since = "2020-02-01",until = "2020-03-20").items(100):
			print(tc)
			tweet = json.dumps(tweet._json)
			tweet = json.loads(tweet)
			tweets.append(tweet)
			tc+=1
		with open("data.json",'w') as file:
			for tweet in tweets:
				json.dump(tweet,file)
				file.write('\n')
	
	def print_tweets(self):

		with open("data.json",'r') as file:
			tweets = file.readlines()

	def divide_tweets(self):
		rumours =[]
		true = []
		with open("data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				if (len(tweet["entities"]["user_mentions"])>0):
					true.append(tweet)
				else:
					rumours.append(tweet)


		with open("true.json",'w') as file:
			for tweet in true:
				json.dump(tweet,file)
				file.write('\n')

		with open("rumours.json",'w') as file:
			for tweet in rumours:
				json.dump(tweet,file)
				file.write('\n')





pur = Maujpur("Maujpur")
#pur.collect_tweets()
pur.divide_tweets()
