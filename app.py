#!/usr/bin/python3

import datetime
import praw
import json

def checkPosts():
    for post in subreddit:
        if not post.stickied:
            print(post.title + " " + str(post.created_utc));

def importConfig():
    global config
    file = open("config.json")
    config = json.load(file)
    file.close()

importConfig()

reddit = praw.Reddit(client_id = config["reddit"]["clientId"], 
    client_secret = config["reddit"]["clientSecret"], 
    user_agent = config["reddit"]["userAgent"]);

for subredditIndex in range( len(config["search"]["subreddit"]) ):
    subreddit = list(config["search"]["subreddit"][subredditIndex].keys())[0];
    

#subreddit = reddit.subreddit("GunAccessoriesForSale").new(limit = 25);
#
#checkPosts();
