# RedditPostNotification
A program which will alert a user of of posts which are made in a specific subreddit if it matches specific search criteria.

A subreddit is queried at most once per second as per Reddit's API rules.

# How to use
1. You need a reddit account (free, no email required) to get an application ID and secret in order to connect to the Reddit API (https://www.reddit.com/prefs/apps/)
2. You will need a slack account, create a workspace, and a webhook to send notifications (https://api.slack.com/messaging/webhooks)
3. Create a `config.json` file to store the credentials (refer to the config example)
4. Modify the `config.json` to include subreddits and keyword filters which you want to be notified about
5. Build and run the script
    * clone the repository
    * `cd RedditPostNotification`
    * `pip3 install slack-webhook` (https://pypi.org/project/slack-webhook/)
    * `python3 app.py`

# Todo
1. if the repo is updated the program should prompt the user to update
2. output the matches to a log file
3. create thorough documentation and video when core functionality is complete
4. Add error messages and test

# Dependencies
1. Reddit account (free and doesn't require email)
2. Slack account (free)
3. Python v3.6+
