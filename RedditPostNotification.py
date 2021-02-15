#!/usr/bin/python3

import datetime, praw, json, time, requests

def importConfig():
    global config
    file = open("config.json")
    config = json.load(file)
    file.close()

# returns a time stamp for the logs
def getTimeStamp():
    now = datetime.datetime.now()
    date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)

    if now.hour > 12:
        time = str(now.hour - 12) + ":" + str(now.minute).zfill(2) + " PM"
    else:
        time = str(now.hour) + ":" + str(now.minute).zfill(2) + " AM"

    timeStamp = date + " " + time
    return timeStamp

# creates string to be output to the log and console
def createResultOutput(post, subreddit):
    message = getTimeStamp() + " - " + subreddit + " - " + post.title
    return message

# creates payload and sends post request to slack
def postToSlack(users, post):
    message = {
        "text": post.title,
        "blocks": [
	        {
		        "type": "section",
		        "text": {
			        "type": "mrkdwn",
			        "text": "<https://reddit.com" + post.permalink + "|" + post.title + ">"
		        }
	        }
        ]
    }

    # adds users to be notified of post to message
    if (users != ""):
        message["blocks"][0]["text"]["text"] = users + message["blocks"][0]["text"]["text"]

    # sends message to slack
    response = requests.post(
        webhookUrl, data=json.dumps(message),
        headers={'Content-Type': 'application/json'}
    )

# writes found post to the results.log file
def outputResultToLog(message, url):
    f = open("results.log", "a")
    f.write(message + " (" + url + ")\n")
    f.close()

# writes found post to the errors.log file
def outputErrorToLog(message, error):
    print(message + "\n" + str(e))
    f = open("errors.log", "a")
    f.write( getTimeStamp() + ": " + message + "\n" + str(error) + "\n\n")
    f.close()

# reads the config to determine who to notify for the specfic filter
def determineWhoToNotify(filter):
    result = ""

    if (filter.get("notify")):
        whoToNotify = list(filter["notify"])
        
        for user in whoToNotify:
            result += "<@" + user + "> "

    return result

# determines if the reddit post title contains every word in the filter list
def stringContainsEveryElementInList(keywordList, string):
    inList = True # default
    for keyword in keywordList:
        if keyword not in string:
                inList = False
    return inList

try:
    importConfig() # reads from config.json
except FileNotFoundError as e:
    simpleErrorMessage = "Error: config.json is not found, create it based on the example_config.json"
    outputErrorToLog(simpleErrorMessage, e)
    quit() # terminates program
except ValueError as e:
    simpleErrorMessage = "Error: config.json is not formatted correctly"
    outputErrorToLog(simpleErrorMessage, e)
    quit() # terminates program
except Exception as e:
    simpleErrorMessage = "Error: Unhandled exception with regard to importing config"
    outputErrorToLog(simpleErrorMessage, e)
    quit() # terminates program

webhookUrl = str(config["slack"]["webhook-url"])

# access to reddit api
reddit = praw.Reddit(client_id = config["reddit"]["clientId"],
    client_secret = config["reddit"]["clientSecret"],
    user_agent = config["reddit"]["userAgent"])

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
            subredditObj = reddit.subreddit(subreddit).new(limit = 5)
            
            for post in subredditObj:

                if post.created_utc > mostRecentPostTime:
                    mostRecentPostTime = post.created_utc

                if ( post.created_utc > lastSubmissionCreated[str(subreddit)] ):
                    numberOfFilters = len(config["search"][subreddit]["filters"])

                    for filterIndex in range(numberOfFilters):
                        keywordFilter = list([x.lower() for x in config["search"][subreddit]["filters"][filterIndex]["keywords"]])

                        if stringContainsEveryElementInList(keywordFilter, post.title.lower()):
                            message = createResultOutput(post, subreddit)
                            print(message) # shows notification in the console
                            outputResultToLog(message, "https://reddit.com" + post.permalink) # writes to log file
                            postToSlack(determineWhoToNotify(config["search"][subreddit]["filters"][filterIndex]), post) # sends notification to slack

            lastSubmissionCreated[str(subreddit)] = mostRecentPostTime
            time.sleep(1.1)
        except requests.exceptions.ConnectionError as e:
            simpleErrorMessage = "Error: Max retries exceeded before connection established, pausing program for 5 secs and continuing"
            outputErrorToLog(simpleErrorMessage, e)
            time.sleep(5)
        except requests.exceptions.HTTPError as e:
            simpleErrorMessage = ""
            outputErrorToLog(simpleErrorMessage, e)
            time.sleep(5)
        except Exception as e:
            simpleErrorMessage = "Error: Unhandled Exception"
            outputErrorToLog(simpleErrorMessage, e)
            time.sleep(5)

