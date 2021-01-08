#		Harkishan Singh : 2017233 ,		Mayank Chopra : 2017066,		Aman Gulia : 2017328
#		READ report first

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


#		Authenticating
auth = tp.OAuthHandler(tc.API_KEY, tc.API_SECRET_KEY)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_SECRET_TOKEN)


api=tp.API(auth)



#os.mkdir("tweets")

class prof:

	def __init__(self,username):
		self.username = username	
		#self.collect_tweets()
		self.tweets_list = self.get_tweets()
		
		

	def collect_tweets(self):

		tweets = []
		date1 = datetime(2018,12,1,0,0,0,0,pytz.UTC)
		tc = 0

		for status in tp.Cursor(api.user_timeline, id=self.username).items():
			json_str = json.dumps(status._json)
			json_str = json.loads(json_str)
			if(self.username == "ponguru"):
				date = datetime.strptime(json_str['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
				if(date<date1):
					break

				elif (date>date1):
					tweets.append(json_str)
			else :
				tweets.append(json_str)
		


		path = os.path.join("tweets",self.username+".json")
		with open(path,'w') as file:
			for tweet in tweets:
				json.dump(tweet,file)
				file.write('\n')

		print("Data collected successfully")

	def get_tweets(self):

		tweets_list = []
		path = os.path.join("tweets",self.username+".json")
		with open(path,'r') as file:
			for line in file:
				cp = line[:-1]
				tweets_list.append(cp)

		for i in range(len(tweets_list)):
			json_str = json.dumps(tweets_list[i])
			json_str = json.loads(tweets_list[i])
			tweets_list[i]= json_str

		return tweets_list

	def print_tweets(self):
		print(self.tweets_list[0]['created_at'])

	def travel_tweet(self,travel_tweet):

		path = os.path.join("travel",self.username+".json")
		with open(path,'w') as file:
			for tweet in travel_tweet:
				json.dump(tweet,file)
				file.write("\n")


	def conference_tweet(self,conference_tweets):

		path = os.path.join("conference",self.username+".json")
		with open(path,'w') as file:
			for tweet in conference_tweets:
				json.dump(tweet,file)
				file.write("\n")

	def award_tweet(self,award_tweets):
		path = os.path.join("award",self.username+".json")
		with open(path,'w') as file:
			for tweet in award_tweets:
				json.dump(tweet,file)
				file.write("\n")

	def print_sample(self,lt):
		print("\n\n\tTwitter = @",self.username)

		for i in range(len(lt)):
			print("Tweeted on = ",lt[i]['created_at'],"\nTweet = ",lt[i]['text'])
			print("\n")

	def retweeters_list(self):

		retweet_users = []
		path = os.path.join("tweets",self.username+".json")
		with open(path,'r') as file:
			tweets = file.readlines()
			date = datetime(2019,6,25,0,0,0,0,pytz.UTC)
			add = timedelta(1*365/12)
			date1 = date - add
			print("date1= ",date1)
			six_months = []
			for tweet in tweets:
				tweet = json.loads(tweet)	
				tweet_date = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
				print(tweet_date)
				if(tweet_date>date1 and tweet_date<date and tweet["retweet_count"]>0):
					retweeters = api.retweets(id = tweet["id"])
					for person in retweeters:
						person = json.dumps(person._json)
						person = json.loads(person)
						six_months.append(person['user']['screen_name'])
				elif(tweet_date<date1):
					break

			path = os.path.join("retweeters",self.username+".txt")
			with open(path,'a') as f:
				for person in six_months:
					f.write(person+" ")
				f.write("\n")


#	FOR TRAVEL TWEETS


def get_travel_tweets(tweets_list):

	travel_keywords = ['at','travel','travelling','journey','trip','city','country','beauty','beautiful','visited','visit','reached','excited']
	travel_tweets = []

	for tweet in tweets_list:
		for key in travel_keywords:
			text = tweet['text'].split()
			truth = key in text	
			if(truth):
				travel_tweets.append(tweet)
				break
	return travel_tweets

#	FOR CONFERENCE TWEETS


def get_conference_tweets(tweets_list):
	conference_keywords = ['attended','conference','gave','talk']
	conference_tweets = []
	for tweet in tweets_list:
		for key in conference_keywords:
			text = tweet['text'].split()
			truth = key in text	
			if(truth):
				conference_tweets.append(tweet)
				break
	return conference_tweets

#	FOR AWARD TWEETS

def get_award_tweets(tweets_list):
	award_keywords = ['won','win','winner','got','award','recieved']
	award_tweets = []
	for tweet in tweets_list:
		for key in award_keywords:
			text = tweet['text'].split()
			truth = key in text	
			if(truth):
				award_tweets.append(tweet)
				break
	return award_tweets


def engaged():
	path = os.path.join("retweeters","ponguru.txt")
	with open(path,"r") as file:
		users = file.readlines()
	users[0] = users[0].split()
	print(len(users[0]))
	l = []
	for i in range(len(users[0])):
		d = 0
		for j in range(len(l)):
			if(users[1][i]==l[j][0]):
				l[j][1] += 1
				d = 1
				break
		if (d == 0):
			l.append([users[0][i],1])

	for i in range(3):
		m=0
		for j in range(len(l)):
			if(l[j][1]>m):
				m=l[j][1]
				ind = j
		print(l[ind])
		l.pop(ind)


pk = prof("ponguru")
arjun = prof("arjunraycompbio")
ojas = prof("_ojaswa_")


#		Question 1

#		FOR TRAVEL TWEETS

pk_tweets_list = pk.tweets_list
pk_travel_tweets = get_travel_tweets(pk_tweets_list)
#pk.travel_tweet(pk_travel_tweets)
#pk.print_sample(pk_travel_tweets)


arjun_tweets_list = arjun.tweets_list
arjun_travel_tweets = get_travel_tweets(arjun_tweets_list)
arjun.travel_tweet(arjun_travel_tweets)
#arjun.print_sample(arjun_travel_tweets)

ojas_tweets_list = ojas.tweets_list
ojas_travel_tweets = ojas.tweets_list
#ojas.travel_tweet(ojas_travel_tweets)



#		FOR CONFERENCE TWEETS 


pk_conference_tweets = get_conference_tweets(pk_tweets_list)
#pk.conference_tweet(pk_conference_tweets)
#pk.print_sample(pk_conference_tweets)

arjun_conference_tweets = get_conference_tweets(arjun_tweets_list)
arjun.conference_tweet(arjun_conference_tweets)
#arjun.print_sample(arjun_conference_tweets)

ojas_conference_tweets = get_conference_tweets(ojas_tweets_list)
#ojas.conference_tweet(ojas_conference_tweets)


#		FOR AWARD TWEETS

pk_award_tweets = get_award_tweets(pk_tweets_list)
pk.award_tweet(pk_award_tweets)
#pk.print_sample(pk_award_tweets)

arjun_award_tweets = get_award_tweets(arjun_tweets_list)
arjun.award_tweet(arjun_award_tweets)
#arjun.print_sample(get_award_tweets)

ojas_award_tweets = get_award_tweets(ojas_tweets_list)
ojas.award_tweet(ojas_award_tweets)


#ojas.retweeters_list()
#arjun.retweeters_list()
#pk.retweeters_list()
#engaged()

print("READ REPORT!!!")



















