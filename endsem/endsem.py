# Harkishan Singh (2017233)  Mayank Chopra (2017066)  Aman Gulia (2017328)
import csv
import os
import tweepy as tp 
from twitter import Twitter
import tw_cred as tc
import numpy as np 
import json
import matplotlib.pyplot as plt
import json
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time
import pytz
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt
import spacy

auth = tp.OAuthHandler(tc.API_KEY, tc.API_SECRET_KEY)
auth.set_access_token(tc.ACCESS_TOKEN, tc.ACCESS_SECRET_TOKEN)
api=tp.API(auth)

df = pd.read_csv("raw_data1.csv")

def a_create_graph(source):
    l = []
    for source in df[source]:
        try:
            tail = source.index('//')+2
            head = source.find('/',8)
            source_name = source[tail:head]
            d = False
            for i in range(len(l)):
                if( l[i][0]==source_name):
                    ind = i
                    d = True
                    break
            if(d):
                l[ind][1]+=1
            else:
                l.append([source_name,1])
        except:
            pass
    l.sort(key = lambda x:x[1],reverse=True)
    return l

def graph(l):
    plt.title("A : Information gathered from Source 3")
    plt.xlabel("Source of information")
    plt.ylabel("Frequency")
    source = [i[0] for i in l]
    freq = [i[1] for i in l]
    plt.bar(source,freq)
    plt.show()

def print_list(l):
    for i in l:
        print(i)


def get_twitter_handle():
    handle = []
    k = 0
    for i in range(len(df)):
        s = 'twitter.com'
        try:
            s1 = df.iloc[i]['Source_1']
            if(s in s1):
                a = s1.index(s)+12
                b = s1.index('/',a)
                h = s1[a:b].lower()
                if (h not in handle):
                    handle.append(h)
        except:
            pass
        try:
            s2 = df.iloc[i]['Source_2']
            if(s in s2):
                a = s2.index(s)+12
                b = s2.index('/',a)
                h = s2[a:b].lower()
                if (h not in handle):
                    handle.append(h)
        except:
            pass

        try:
            s3 = df.iloc[i]['Source_3']
            if(s in s3):
                a = s3.index(s)+12
                b = s3.index('/',a)
                h = s3[a:b].lower()
                if (h not in handle):
                    handle.append(h)
        except:
            pass

        print(k)
        k+=1
            
    return handle

def get_recent_ten_tweets(handles):
    all_user_tweets = []
    for user in handles:
        print(user)
        tweets = api.user_timeline(id=user,exclude_replies = True,count = 10)
        for tweet in tweets:
            json_str = json.dumps(tweet._json)
            json_str = json.loads(json_str)
            all_user_tweets.append([json_str['created_at'],json_str['text'],user])

    all_user_tweets.sort(key = lambda x :x[0],reverse = True)
    with open('tweets.csv','w') as file:
        reader = csv.writer(file)
        for tweet in all_user_tweets:
            reader.writerow(tweet)

def show_top_ten():
    with open ('tweets.csv','r') as file:
        reader = csv.reader(file)
        i = 1
        for row in reader:
            print("Tweet Created on = ",row[0],"User = ",row[2],"\nTweet : \n",row[1],"\n\n\n")
            if(i==10):
                break
            i+=1

def show_wordcloud():
    text = ''
    with open('tweets.csv','r') as file:
        reader = csv.reader(file)
        for row in reader:
            text = text+" "+row[1]
    w = ['https','.com','com','co','RT','amp']
    for i in w:
        print(i)
        text = text.replace(i,'')

    stopwords = set(STOPWORDS)
    wc = WordCloud(width = 800, height = 800, 
            background_color ='white', 
            stopwords = stopwords, 
            min_font_size = 10).generate(text)

    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wc) 
    plt.axis("off") 
    plt.tight_layout(pad = 0)
    plt.show() 

def get_verified_unverified():
    users = []
    with open('tweets.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            user = row[2]
            if (user not in users):
                users.append(user)
    print(users)
    verified = []
    unverified = []
    for user in users:
        print(user)
        tweet = api.user_timeline(id=user,exclude_replies = True,count = 1)[0]
        json_str = json.dumps(tweet._json)
        json_str = json.loads(json_str)
        if(json_str['user']['verified']):
            verified.append(user)
        else:
            unverified.append(user)

    with open('verified.csv','w') as file:
        writer = csv.writer(file)
        for user in verified:
            writer.writerow([user])
    with open('unverified.csv','w') as file:
        writer = csv.writer(file)
        for user in unverified:
            writer.writerow([user])

def maximum_posts():
    handle = []
    k = 0
    for i in range(len(df)):
        s = 'twitter.com'
        try:
            s1 = df.iloc[i]['Source_1']
            if(s in s1):
                a = s1.index(s)+12
                b = s1.index('/',a)
                h = s1[a:b].lower()
                handle.append(h)
        except:
            pass
        try:
            s2 = df.iloc[i]['Source_2']
            if(s in s2):
                a = s2.index(s)+12
                b = s2.index('/',a)
                h = s2[a:b].lower()
                handle.append(h)
        except:
            pass

        try:
            s3 = df.iloc[i]['Source_3']
            if(s in s3):
                a = s3.index(s)+12
                b = s3.index('/',a)
                h = s3[a:b].lower()
                handle.append(h)
        except:
            pass

    unique_handle = []
    for user in handle:
        d = 0
        
        for u in range(len(unique_handle)):
            if(unique_handle[u][0]==user):
                d=1
                ind = u
                break
        if(d == 0):
            unique_handle.append([user,1])
        else:
            unique_handle[ind][1]+=1
    
    return unique_handle

def location():
    nlp = spacy.load('en_core_web_sm')
    total = 0
    for i in range(len(df)):
        try:
            st = df.iloc[i]['Notes']
            doc = nlp(st)
            place = []
            for ent in doc.ents:
                if(ent.label_ == 'GPE'):
                    place.append(ent.text)
            try:
                if(df.iloc[i]['Detected City'] in place):
                    total+=1
                    continue
            except: 
                pass
            
            try:
                if(df.iloc[i]['Detected State'] in place):
                    total+=1
                    continue
            
            except:
                pass
            



        except:
            pass
        print(i)
    return total



#source_1 = a_create_graph('Source_1')
#source_2 = a_create_graph('Source_2')
#source_3 = a_create_graph('Source_3')
#print_list(source_3)
#graph(source_3)

#handles = get_twitter_handle()
#print("Total number of twitter users : ",len(handles))
#print(handles)
#get_recent_ten_tweets(handles)
#show_top_ten()
#show_wordcloud()

#get_verified_unverified()
#m = maximum_posts()
#print_list(m)