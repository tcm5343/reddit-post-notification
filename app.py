#!/usr/bin/python3

import datetime, praw, json, time, requests

def importConfig():
    global config
    file = open("config.json")
    config = json.load(file)
    file.close()

# creates string to be output to the log and console    
def createOutput(post, subreddit):
    now = datetime.datetime.now()
    date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)
    time = ""

    if now.hour > 12:
        time = str(now.hour - 12) + ":" + str(now.minute).zfill(2) + " PM"
    else:
        time = str(now.hour) + ":" + str(now.minute).zfill(2) + " AM"

    message = date + " " + time + " - " + subreddit + " - " + post.title
    return message

def postToSlack(post):
    message = {
        "blocks": [
	        {
		        "type": "section",
		        "text": {
			        "type": "mrkdwn",
			        "text": "<" + post.url + "|" + post.title + ">"
		        }
	        }
        ]
    }

    response = requests.post(
        webhookUrl, data=json.dumps(message),
        headers={'Content-Type': 'application/json'}
    )

# writes found post to the log.log file
def outputToLog(message, url):
    f = open("log.log", "a")
    f.write(message + " (" + url + ")\n")
    f.close()

def stringContainsEveryElementInList(keywordList, string):
    inList = True # default
    for keyword in keywordList:           
        if keyword not in string:
                inList = False
    return inList

  
importConfig() # reads from config.json   
webhookUrl = str(config["slack"]["webhook-url"])

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
        try:
            mostRecentPostTime = 0 # stores most recent post time of this batch of posts

            # returns new posts from subreddit
            subredditObj = reddit.subreddit(subreddit).new(limit = 5);
            #print("call to subreddit " + subreddit)
            for post in subredditObj:

                if post.created_utc > mostRecentPostTime:
                    mostRecentPostTime = post.created_utc

                if ( post.created_utc > lastSubmissionCreated[str(subreddit)] ):
                    numberOfFilters = len(config["search"][subreddit]["filters"])

                    for filterIndex in range(numberOfFilters):
                        keywordFilter = list([x.lower() for x in config["search"][subreddit]["filters"][filterIndex]["keywords"]])

                        if stringContainsEveryElementInList(keywordFilter, post.title.lower()):
                            message = createOutput(post, subreddit) 
                            
                            outputToLog(message, post.url) # writes to log file
                            postToSlack(post) # sends notification to slack
                            print(message) # shows notification in the console
                            
            lastSubmissionCreated[str(subreddit)] = mostRecentPostTime
            time.sleep(1.1)
        except Exception as e:
            print(e)
            time.sleep(5)
