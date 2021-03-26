#!/usr/bin/python3

import datetime, praw, json, time, requests

def importConfig() -> None:
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
def getTimeStamp(now) -> str:
    date = str(now.month) + "-" + str(now.day) + "-" + str(now.year)

    if now.hour == 11:
        time = "12" + ":" + str(now.minute).zfill(2) + " PM"
    elif now.hour > 11:
        time = str(now.hour - 12) + ":" + str(now.minute).zfill(2) + " PM"
    elif now.hour == 0:
        time = "12" + ":" + str(now.minute).zfill(2) + " AM"
    else:
        time = str(now.hour) + ":" + str(now.minute).zfill(2) + " AM"

    timeStamp = date + " " + time
    return timeStamp

# creates string to be output to the log and console
def createResultOutput(post, subreddit) -> str:
    message = getTimeStamp(datetime.datetime.now()) + " - " + subreddit + " - " + post.title
    return message

# creates payload and sends post request to the notification app
def sendNotification(users, post, notification_app) -> None:
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
def outputResultToLog(message, url) -> None:
    f = open("results.log", "a")
    f.write(message + " (" + url + ")\n")
    f.close()

# writes found post to the errors.log file
def outputErrorToLog(message, error) -> None:
    print(message + "\n" + str(e))
    f = open("errors.log", "a")
    f.write( getTimeStamp(datetime.datetime.now()) + ": " + message + "\n" + str(error) + "\n\n")
    f.close()

# reads the config to determine who to notify for the specfic filter
def determineWhoToNotify(filter) -> list:
    result = []    
    if (filter.get("notify")):
        for user in list(filter["notify"]):
            result.append(user)
    return result

# determines if a string contains every word in a list of strings
# not case-sensitive
def stringContainsEveryElementInList(keywordList, string) -> bool:
    inList = True # default
    if not keywordList: # if list is empty
        inList = False
    else: # list is not empty
        for keyword in list([x.lower() for x in keywordList]):
            if keyword not in string.lower():
                    inList = False
    return inList

# determines if a string contains at least one word in a list of strings
# not case-sensitive
def stringContainsAnElementInList(keywordList, string) -> bool:
    inList = False # default
    for keyword in list([x.lower() for x in keywordList]):
        if keyword in string.lower():
                return True
    return inList

def main() -> None:
    importConfig() # reads from config.json

    # determine which notification app to use
    notification_app = str(config["notifications"]["app"])

    # access to reddit api
    reddit = praw.Reddit(client_id = config["reddit"]["clientId"],
        client_secret = config["reddit"]["clientSecret"],
        user_agent = "default")

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
                                includesFlag = stringContainsEveryElementInList(filter["includes"], post.title)
                            else: 
                                includesFlag = True

                            if (filter.get("except")):
                                exceptFlag = stringContainsAnElementInList(filter["except"], post.title)
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

if __name__ == "__main__":
    main()
    