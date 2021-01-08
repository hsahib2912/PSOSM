import numpy as np 
import json
import tweepy as tp 
import tw_cred as tc
import csv
from datetime import datetime
from datetime import timedelta
import time
import pytz
import matplotlib.pyplot as plt
import os
from calendar import monthrange
from wordcloud import WordCloud, STOPWORDS 

#		Authenticating
auth = tp.OAuthHandler(tc.API_KEY, tc.API_SECRET_KEY)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_SECRET_TOKEN)


api=tp.API(auth)

class camila:

	def __init__(self):
		self.username = "camila_cabello"

	def get_data(self):
		date1 = datetime(2018,12,1,0,0,0,0,pytz.UTC)
		date2 = datetime(2020,1,25,0,0,0,0,pytz.UTC)
		print(date1)
		#print(date1<date2)
		tweets_list = []
		print("Collecting data")
		for status in tp.Cursor(api.user_timeline, id=self.username).items():
			json_str = json.dumps(status._json)
			json_str = json.loads(json_str)
			date = datetime.strptime(json_str['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
			
			if(date<date1):
				break

			elif (date>date1 and date<date2):
				tweets_list.append(json_str)

		with open("Camila_data.json",'a') as file:
			for tweet in tweets_list:
				json.dump(tweet,file)
				file.write('\n')
		print("Data collected successfully")


	def print_recent_five(self):
		tweets_list = []
		with open("Camila_data.json") as file:
			for line in file:
				cp = line[:-1]
				tweets_list.append(cp)
		
		print("\n\n\t\t5 Sample tweets from collected data : ")
		for i in range(5):
			
			json_str = json.dumps(tweets_list[i])
			json_str = json.loads(tweets_list[i])
			print("\t\tTweeted at : ",json_str['created_at'])
			print("\t\tTweet :      ",json_str['text'],"\n\n")


	def follower_list (self):

		followers = api.followers_ids(self.username)
		with open("Followers.txt",'w') as file:
			for follower in followers:
				file.write("%s\n" % follower)


	def plot_followers(self):

		followers_ids=[]
		with open("Followers.txt") as file:
			for line in file:
				cp = line[:-1]
				followers_ids.append(int(cp))

		end = 100
		l=[]
		while(end<len(followers_ids) and end<1000):
			follower = api.lookup_users(user_ids = followers_ids[end-100:end])
			for i in follower:
				i = json.dumps(i._json)
				i = json.loads(i)
				if(i['location']!=''):
					print(i['location'])
					l.append(i['location'])
				
			end+=100

		rep = []
		for i in range(len(l)):
			d=0
			for j in range(len(rep)):
				if (l[i]==rep[j][0]):
					rep[j][1]=rep[j][1]+1
					d = 1
					break
			if (d==0):
				rep.append([l[i],1])

		places = []
		mag = []

		rep = sort_list(rep)

		y_pos = np.arange(5)

		for i in range(5):
			places.append(rep[i][0])
			mag.append(rep[i][1])

		plt.bar(y_pos,mag,align = 'center', alpha = 0.5)
		plt.xticks(y_pos,places)
		plt.ylabel('Number of followers')
		plt.title('Question 2')
		plt.show()
		
	def no_retweets(self):
		tweets_list=[]
		with open("Camila_data.json") as file:
			for line in file:
				cp = line[:-1]
				tweets_list.append(cp)

		rt = 0
		for i in range(len(tweets_list)):
			json_str = json.dumps(tweets_list[i])
			json_str = json.loads(tweets_list[i])
			rt += json_str["retweet_count"]
			
		print(rt)

	def list_of_retweeters(self):
		pass

	def get_tweets_list(self):
		pass

	def retweeters_list(self):
		retweet_users = []
		path = os.path.join("Camila_data.json")
		with open(path,'r') as file:
			tweets = file.readlines()
			date = datetime(2019,6,25,0,0,0,0,pytz.UTC)
			add = timedelta(days = 10)
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
			with open("retweeters.txt",'w') as f:
				for person in six_months:
					f.write(person+" ")
				f.write("\n")

	def tweets_freq(self):
		n_tweets = []
		mnt = []
		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			n = 0
			abs_lb = datetime(2019,1,1,0,0,0,0,pytz.UTC)
			lb = datetime(2019,12,1,0,0,0,0,pytz.UTC)
			ub = datetime(2020,1,1,0,0,0,0,pytz.UTC)
			for tweet in tweets:
				tweet = json.loads(tweet)
				tweet_date = datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y').replace(tzinfo=pytz.UTC)
				if (tweet_date>ub):
					continue
				elif(tweet_date>lb and tweet_date<ub):
					n+=1

				elif (tweet_date<abs_lb):
					n_tweets.append(n)
					mnt.append(lb.month)
					break
				elif (tweet_date<lb and tweet_date<ub):
					n_tweets.append(n)
					mnt.append(lb.month)
					sub1 = timedelta(days = monthrange(2019,lb.month-1)[1])
					sub2 = timedelta(days = monthrange(2019,lb.month)[1])
					lb = lb-sub1
					ub = ub-sub2
					n = 0
		print(n_tweets)
		print(mnt)

		n_tweets.reverse()
		mnt.reverse()

		graph(mnt,n_tweets)

		y_tweets = 0
		for i in n_tweets:
			y_tweets+= i
		print("Total number of tweets in year 2019 by Camila = ",y_tweets)

		print ("Frequency of tweets = ",y_tweets/12," per month")
		print ("Frequency of tweets = ",y_tweets/365," per day")

	def score(self):
		score =0
		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				print(tweet)
				print(tweet['entities']['media'])
				break
				likes = tweet['favorite_count']
				rt = tweet['retweet_count']
				score+= (likes+rt)/977
		print("Score = ", score)

	def wc(self):

		st = ''
		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				if(tweet['text'].find('http')==-1):
					st = st + " "+ tweet['text']


		stopwords = set(STOPWORDS)
		wc = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = stopwords, 
                min_font_size = 10).generate(st)

		plt.figure(figsize = (8, 8), facecolor = None) 
		plt.imshow(wc) 
		plt.axis("off") 
		plt.tight_layout(pad = 0)
		plt.show() 

	def hash(self):

		htags = []
		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				
				if(len(tweet['entities']['hashtags'])!=0):
					for j in range(len(tweet['entities']['hashtags'])):
						htags.append(tweet['entities']['hashtags'][0]['text'])

		rep = []
		for i in range(len(htags)) :
			d=0
			for j in range(len(rep)):
				if(rep[j][0]==htags[i]):
					rep[j][1]+=1
					d=1
					break
			if(d==0):
				rep.append([htags[i],1])

		rep = sort_list(rep)
		print("Top 10 hasttags used by Camila in her tweets are : ")
		for i in range(10):
			print(rep[i])

		htag = []
		freq = []
		for i in range(10):
			htag.append(rep[i][0])
			freq.append(rep[i][1])

		graph(htag,freq)

	def tweet_len(self):

		t_len = []
		su = 0

		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				print(tweet)
				tlen = len(tweet['text'])
				if (tlen>140):tlen=140
				su+= tlen 
				t_len.append(tlen)

		print("Maximum length of tweet by Camila = ",max(t_len))
		print("Average length of Camila tweet = ",su/977)

		x = np.arange(len(t_len[:100]))
		plt.plot(x,t_len[:100])
		plt.xlabel("Tweet")
		plt.ylabel("Length of tweet")
		plt.show()

	def text(self):
		text_tweets = []
		like = 0
		rt = 0 
		total = 0
		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				try:
					len(tweet['entities']['media'])

				except:
					text_tweets.append(tweet)
					like+= tweet['favorite_count']
					rt+= tweet['retweet_count']
					total+=1
		
		print("Average like on a tweet containing only text =",like/total)
		print("Average retweet on a tweet containing only text =",rt/total)
		
	def media(self):
		media_tweets = []
		like = 0
		rt = 0 
		total = 0
		with open("Camila_data.json",'r') as file:
			tweets = file.readlines()
			for tweet in tweets:
				tweet = json.loads(tweet)
				try:
					len(tweet['entities']['media'])
					total+=1
					media_tweets.append(tweet)
					like+= tweet['favorite_count']
					rt+= tweet['retweet_count']

				except:
					continue
		
		print("Average like on a tweet containing only text =",like/total)
		print("Average retweet on a tweet containing only text =",rt/total)




def sort_list(lt):  
	lt.sort(key = lambda x: x[1],reverse = True)  
	return lt

def engaged():
	path = os.path.join("retweeters.txt")
	with open(path,"r") as file:
		users = file.readlines()
	users[0] = users[0].split()
	print(len(users[0]))
	l = []
	for i in range(len(users[0])):
		d = 0
		for j in range(len(l)):
			if(users[0][i]==l[j][0]):
				l[j][1] += 1
				d = 1
				break
		if (d == 0):
			l.append([users[0][i],1])

	lt_users = [] 
	for i in range(10):
		m=0
		for j in range(len(l)):
			if(l[j][1]>m):
				m=l[j][1]
				ind = j
		lt_users.append(l[ind])
		l.pop(ind)

	user = []
	rt = []
	y_pos = np.arange(10)
	for i in range(10):
		user.append(lt_users[i][0])
		rt.append(lt_users[i][1])

	plt.bar(y_pos,rt,align = 'center', alpha = 0.5)
	plt.xticks(y_pos,users)
	plt.ylabel('Number of retweets')
	plt.title('Question 3')
	plt.show()
	return user

def visualize(users):


	person = api.lookup_users(screen_names = users)

	follower = []
	following = []
	location = []
	for i in person:
		i = json.dumps(i._json)
		i = json.loads(i)
		follower.append(i['followers_count'])
		following.append(i['friends_count'])
		location.append([i['screen_name'],i['location']])

	for i in range(10):
		print(location[i])
	graph(users,following)



def graph(users,lt):
	y_pos = np.arange(10)
	plt.bar(y_pos,lt,align = 'center', alpha = 0.5)
	plt.xticks(y_pos,users)
	plt.ylabel('Number of time hashtags used')
	plt.xlabel('Hashtag')
	plt.title('Question 6')
	plt.show()

	


print("Hello")
cam = camila()
#cam.get_data()
#cam.print_recent_five()
#cam.follower_location()
#cam.plot_followers()
#cam.retweeters_list()
#cam.no_retweets()
#lt = engaged()
#visualize(lt)
#cam.tweets_freq()
#cam.score()
#cam.wc()
#cam.hash()
#cam.tweet_len()
#cam.text()
#cam.media()


