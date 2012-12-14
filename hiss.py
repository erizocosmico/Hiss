#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
The MIT License

Copyright (c) 2012 José Miguel Molina <rd4091@gmail.com> <@_mvader>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import urlparse, os, json, urllib, time
import oauth2 as oauth
from hiss_config import get_config

consumer_key, consumer_secret, style, num_tweets = get_config()
request_token_url = 'http://twitter.com/oauth/request_token'
access_token_url = 'http://twitter.com/oauth/access_token'
authorize_url = 'http://twitter.com/oauth/authorize'
consumer = oauth.Consumer(consumer_key, consumer_secret)
get_timeline_url = "https://api.twitter.com/1/statuses/home_timeline.json?include_entities=false&count=" + str(num_tweets)
last_id = 1
if style:
    color_scheme = []
else:
    color_scheme = []

def twitter_auth():
    f = open('token.txt', 'r')
    content = f.read()
    try:
        tokens = json.loads(content)
    except ValueError:
        print "\033[1;37;41m--- Error loading token, please delete token.txt ---\033[0m"
        exit()
    token = oauth.Token(tokens['oauth_token'], tokens['oauth_token_secret'])
    client = oauth.Client(consumer, token)
    return client
    
def parse_date(date):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str(date),'%a %b %d %H:%M:%S +0000 %Y'))

def timeline(update = False, last_id = 1):
    client = twitter_auth()
    if update and last_id != 1:
        url = get_timeline_url + "&since_id=" + str(last_id)
    else:
        url = get_timeline_url
    resp, tweets = client.request(url, "GET")
    print "\033[1;32m-------------------------------\033[0m"
    status = resp['status']
    if status != '200':
        print "\033[1;37;41m--- Error loading tweets ---\033[0m"
        return last_id
    tweets = json.loads(tweets)
    if type(tweets).__name__ == 'list':
        tweets.reverse()
    for tweet in tweets:
        print '\033[1;37mID#' + str(tweet['id']) + "\033[0m \033[1;36m@" + tweet['user']['screen_name'] + "\033[0m \033[1;37m(" + parse_date(tweet['created_at']) + "):\033[0m"
        print "\033[1;0m" + tweet['text'] + "\033[0m"
        print "\033[1;32m-------------------------------\033[0m"
        last_id = tweet['id']
    return last_id
    
def tweet(tweet, in_reply_to_status_id = 0):
    url = "https://api.twitter.com/1/statuses/update.json"
    client = twitter_auth()
    if in_reply_to_status_id != 0:
        reply = "&in_reply_to_status_id=" + str(in_reply_to_status_id)
    else:
        reply = ""
    data = 'status=' + urllib.quote_plus(tweet) + reply
    resp, content = client.request(url, "POST", data)
    if resp['status'] != '200':
        print "\033[1;37;41m--- Error sending tweet ---\033[0m"
    else:
        print "\033[1;32m--- Tweet sent ---\033[0m"
    
def retweet(rt_id):
    url = "http://api.twitter.com/1/statuses/retweet/" + str(rt_id) + ".json"
    client = twitter_auth()
    resp, content = client.request(url, "POST")
    if resp['status'] != '200':
        print "\033[1;37;41m--- Error retwitting tweet ---\033[0m"
    else:
        print "\033[1;32m--- Tweet retwitted ---\033[0m"
    
def fav_tweet(fav_id):
    url = "https://api.twitter.com/1/favorites/create/" + str(fav_id) + ".json"
    client = twitter_auth()
    resp, content = client.request(url, "POST")
    if resp['status'] != '200':
        print "\033[1;37;41m--- Error faving tweet ---\033[0m"
    else:
        print "\033[1;32m--- Tweet faved ---\033[0m"
    
def block(block_name):
    url = "https://api.twitter.com/1/blocks/create.json"
    client = twitter_auth()
    block_data = "&screen_name=" + block_name + "&include_entities=true"
    resp, content = client.request(url, "POST", block_data)
    if resp['status'] != '200':
        print "\033[1;37;41m--- Error blocking user ---\033[0m"
    else:
        print "\033[1;32m--- User blocked ---\033[0m"
    
def report(report_name):
    url = "http://api.twitter.com/1/report_spam.json"
    client = twitter_auth()
    report_data = "&screen_name=" + report_name + "&include_entities=true"
    resp, content = client.request(url, "POST", report_data)
    if resp['status'] != '200':
        print "\033[1;37;41m--- Error reporting user ---\033[0m"
    else:
        print "\033[1;32m--- User reported ---\033[0m"

if os.path.exists('token.txt'):
    print "\033[1;32m-------------------------------\033[0m"
    print "WELCOME TO \033[1;33mHISS\033[0m"
    accepted = 'n'
    accepted = raw_input('Load timeline? (y/n): ')
    if accepted.lower() == 'y':
        print "Loading timeline..."
        print "\033[1;32m-------------------------------\033[0m"
        last_id = timeline()
    else:
        print "\033[1;32m-------------------------------\033[0m"
    while True:
        cmd = raw_input("\033[1;36mEnter command:\033[0m ")
        if (cmd == "help"):
            pass
            # Display help
        elif (cmd == 'r'):
            last_id = timeline(True, last_id)
        elif (cmd == 't'):
            t = str(raw_input('\033[1;36mTweet:\033[0m '))
            tweet(t)
            last_id = timeline(True, last_id)
        elif (cmd == 'to'):
            t = str(raw_input('\033[1;36mTweet:\033[0m '))
            tweet(t)
        elif (cmd == 'rt'):
            rt_id = int(input('\033[1;36mId of the tweet to retweet:\033[0m '))
            retweet(rt_id)
        elif (cmd == 'load'):
            last_id = timeline()
        elif (cmd == 'reply'):
            id_reply = int(input('\033[1;36mId of the tweet to reply:\033[0m '))
            t = str(raw_input('\033[1;36mReply:\033[0m '))
            tweet(t, id_reply)
            last_id = timeline(True, last_id)
        elif (cmd == 'block'):
            block_name = str(raw_input('\033[1;36mUser to block:\033[0m '))
            block(block_name)
        elif (cmd == 'report'):
            report_name = str(raw_input('\033[1;36mUser to report:\033[0m '))
            report(report_name)
        elif (cmd == 'fav'):
            id_fav = int(input('\033[1;36mId of the tweet to fav:\033[0m '))
            fav_tweet(id_fav)
        elif (cmd == 'exit'):
            exit()
    
else:
    client = oauth.Client(consumer)
    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("\033[1;37;41m--- Invalid response: %s ---\033[0m" % resp['status'])
    print "\033[1;32m--- Accessing... ---\033[0m"
    request_token = dict(urlparse.parse_qsl(content))

    print "Go to the following link on your browser:"
    print "%s?oauth_token=%s" % (authorize_url, request_token['oauth_token'])
    print 

    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = raw_input('Have you authorized the application? (y/n): ')
    oauth_verifier = raw_input('Enter the PIN: ')

    token = oauth.Token(request_token['oauth_token'],
        request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urlparse.parse_qsl(content))
    content = json.dumps({'oauth_token': access_token['oauth_token'], 'oauth_token_secret' : access_token['oauth_token_secret']})
    f = open("token.txt", "w")
    f.write(content)
    f.close()
    print "Now you have access to twitter using Hiss. Navigate to hiss directory on your terminal and enter python hiss.py to start tweeting."
