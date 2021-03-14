#!/usr/bin/python3

import datetime, praw, json, time, requests

def importConfig():
    try:
        global config
        file = open("config.json")
        config = json.load(file)
        file.close()
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
def sendNotification(users, post, notification_app):
    if notification_app == "slack":
        formatted_users = ""
        for index, user in enumerate(users):
            formatted_users += "<@" + str(users[index]) + "> "

        api_url = str(config["notifications"]["slack"]["webhook-url"])
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
        if (formatted_users != ""):
            message["blocks"][0]["text"]["text"] = formatted_users + message["blocks"][0]["text"]["text"]

        # sends message to slack
        response = requests.post(
            api_url, data=json.dumps(message),
            headers={'Content-Type': 'application/json'}
        )
    elif notification_app == "telegram":
        for user in users:
            api_url = f'https://api.telegram.org/bot{ str(config["notifications"]["telegram"]["token"]) }/sendMessage'

            message = f'<a href="https://reddit.com{post.permalink}">{post.title}</a>'

            # Create json link with message
            data = {'chat_id': user, 'text': message, 'parse_mode': 'HTML'}

            # POST the message
            requests.post(api_url, data)

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
    result = []    

    if (filter.get("notify")):
        for user in list(filter["notify"]):
            result.append(user)

    return result

# determines if a string contains every word in a list of strings
def stringContainsEveryElementInList(keywordList, string):
    inList = True # default
    for keyword in keywordList:
        if keyword not in string:
                inList = False
    return inList

# determines if a string contains at least one word in a list of strings
def stringContainsAnElementInList(keywordList, string):
    inList = False # default
    for keyword in keywordList:
        if keyword in string:
                return True
    return inList

importConfig() # reads from config.json

# determine which notification app to use
notification_app = str(config["notifications"]["app"])

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

                # updates the time of the most recently filtered post
                if post.created_utc > mostRecentPostTime:
                    mostRecentPostTime = post.created_utc

                # checks the time the post was created vs the most recent logged time to ensure
                # posts are not filtered multiple times
                if ( post.created_utc > lastSubmissionCreated[str(subreddit)] ):
                    numberOfFilters = len(config["search"][subreddit]["filters"])

                    for filterIndex in range(numberOfFilters):
                        # default flag intiliazations
                        exceptFlag = True
                        includesFlag = False
                        
                        filter = config["search"][subreddit]["filters"][filterIndex]

                        if (filter.get("includes")):
                            includesFilter = list([x.lower() for x in filter["includes"]])
                            includesFlag = stringContainsEveryElementInList(includesFilter, post.title.lower())
                        else: 
                            includesFlag = True

                        if (filter.get("except")):
                            exceptFilter = list([x.lower() for x in filter["except"]])
                            exceptFlag = stringContainsAnElementInList(exceptFilter, post.title.lower())
                        else:
                            exceptFlag = False

                        if includesFlag and not exceptFlag:
                            message = createResultOutput(post, subreddit)
                            print(message) # shows notification in the console
                            outputResultToLog(message, "https://reddit.com" + post.permalink) # writes to log file
                            sendNotification(determineWhoToNotify(filter), post, notification_app) # sends notification to slack

            lastSubmissionCreated[str(subreddit)] = mostRecentPostTime
            time.sleep(1.1)
        except Exception as e:
            outputErrorToLog(" ", e)
            time.sleep(5)
