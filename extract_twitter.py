#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import tweepy
import requests
from textblob import TextBlob
from googletrans import Translator
from unidecode import unidecode
 
# Path to save sentimental analisys 
negativeWordsPath = './store/negative.txt'
positiveWordsPath = './store/positive.txt'
neutralWordsPath = './store/neutral.txt'
  
# Configure Twitter credentials
consumer_key = '<consumer_key>'
consumer_secret = '<consumer_secret>'
access_token = '<access_token>'
access_token_secret = '<access_token_secret>'
  
auth=tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

def store(path, word):
    arq = open(path , 'a')
    arq.write(word)
    arq.close()

def showMessage(type, value, textInPortuguese):
    print( "[Tweet] " + textInPortuguese)
    print( "[Polarity ", type, " ] - ", value )


def get_tweets(tcp_connection):
    try:
        for tweet in tweepy.Cursor(api.search,q="#bolsonaro", since = '2019-08-08',lang="pt").items(10):
        textInPortuguese=unidecode(tweet.text) 
        textInEnglish=Translator().translate(textInPortuguese)
        sentiment = TextBlob(textInEnglish.text)
        
        if sentiment.polarity > 0: 
            store(positiveWordsPath, textInPortuguese)
            showMessage("positive", str(sentiment.polarity), textInPortuguese)

        elif sentiment.polarity < 0:
            tcp_connection.sendall(textInPortuguese.encode(')) 
            store(negativeWordsPath, textInPortuguese)
            showMessage("negative", str(sentiment.polarity), textInPortuguese)

        elif sentiment.polarity == 0:
            store(neutralWordsPath, textInPortuguese)
            showMessage("neutral", str(sentiment.polarity), textInPortuguese)

    except BrokenPipeError:
      pass
      

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind(("192.168.43.208", 7035))
s.listen(1)
 
print("Waiting for TCP connection...")
connection, addr = s.accept()
 
print("Connected... Starting getting tweets.")
get_tweets(connection)
