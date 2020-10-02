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
        mostRecentPostTime = 0 # stores most recent post time of this batch of posts

        # returns new posts from subreddit
        subredditObj = reddit.subreddit(subreddit).new(limit = 5);
        print("** New Call **")

        for post in subredditObj:

            if post.created_utc > mostRecentPostTime:
                mostRecentPostTime = post.created_utc

            print(str(subreddit) + ": lastSubmissionTime " + str(lastSubmissionCreated[str(subreddit)]) + "Post created: " + str(post.created_utc))

            if ( post.created_utc > lastSubmissionCreated[str(subreddit)] ):
                numberOfFilters = len(config["search"][subreddit]["filters"])
                print("SDFLKJFDSGLKJ;SDGFL;KJDSGF;LKJDSGF;KJLDGFS;LKJDGFSL;KJDFSGLK;JDSGFLK;JDSGFLK;JDGFS;LKJDSGF")

                for filterIndex in range(numberOfFilters):
                    keywordFilter = list([x.lower() for x in config["search"][subreddit]["filters"][filterIndex]["keywords"]])

                    if stringContainsEveryElementInList(keywordFilter, post.title.lower()):
                        print("found " + post.title)
                        slack.post(text=post.title)

        lastSubmissionCreated[str(subreddit)] = mostRecentPostTime
        time.sleep(2)
