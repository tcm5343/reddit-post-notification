#!/usr/bin/python3

import datetime, praw, json, time
from slack_webhook import Slack

def checkPosts():
    for post in subreddit:
        if not post.stickied:
            print(post.title + " " + str(post.created_utc));

def importConfig():
    global config
    file = open("config.json")
    config = json.load(file)
    file.close()

def stringContainsEveryElementInList(keywordList, string):
    inList = True # default
    for keyword in keywordList:           
        if keyword not in string:
                inList = False
    return inList

  
importConfig() # reads from config.json   

slack = Slack(url = config["slack"]["webhook-url"]) # access to slack webhook

# access to reddit api
reddit = praw.Reddit(client_id = config["reddit"]["clientId"], 
    client_secret = config["reddit"]["clientSecret"], 
    user_agent = config["reddit"]["userAgent"]);

# list holds the names of subreddits to search
subredditNames = list(config["search"].keys())

# stores the time the last submission checked was created in unix time per subreddit
lastSubmissionCreated = {}
for subreddit in subredditNames:
    lastSubmissionCreated[str(subreddit)] = time.time()

while (True):
    for subreddit in subredditNames:

        # returns new posts from subreddit
        subredditObj = reddit.subreddit(subreddit).new(limit = 10);
        print("** New Call **")

        for post in subredditObj:
            scanned = True

            if ( post.created_utc >= lastSubmissionCreated[str(subreddit)] ):
                scanned = False;

            if not post.stickied and not scanned:
                numberOfFilters = len(config["search"][subreddit]["filters"])

                for filterIndex in range(numberOfFilters):
                    keywordFilter = list([x.lower() for x in config["search"][subreddit]["filters"][filterIndex]["keywords"]])

                    if stringContainsEveryElementInList(keywordFilter, post.title.lower()):
                        print("found " + post.title)
                        slack.post(text=post.title)

        lastSubmissionCreated[str(subreddit)] = time.time()
        time.sleep(2)
