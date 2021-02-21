# RedditPostNotification
A program which will alert a user of of posts which are made in a specific subreddit if it matches specific search criteria. Depending on how many subreddits you are checking, a subreddit is queried at most once per second as per Reddit's API rules.

If this program works and saves you some money, consider supporting me by buying me a coffee:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WN85PYVLLLSKL&currency_code=USD)

# How to use
1. You need a reddit account (free, no email required) to get an application ID and secret in order to connect to the Reddit API (https://www.reddit.com/prefs/apps/)
2. You will need a slack account, create a workspace, and a webhook to send notifications (https://api.slack.com/messaging/webhooks)
3. Navigate to your home directory and clone the repo
      * `cd ~`
      * `git clone https://github.com/tcm5343/RedditPostNotification.git`
      * `cd RedditPostNotification`
4. Create `config.json` to store the credentials (refer to `example_config.json`) and place it in RedditPostNotification/
5. Modify the `config.json` to include subreddits and keyword filters which you want to be notified about
6. Run the script
     * Using Docker (Docker must be installed)
          * `sudo docker build -t "redditpostnotification" ./`
          * `sudo docker run --restart unless-stopped --name redditapp -v ~/RedditPostNotification:/usr/src/app -d redditpostnotification`
     * Traditionaly
          * Windows
               * `pip install praw` (https://praw.readthedocs.io/en/latest/)
               * `python RedditPostNotification.py`
          * Linux
               * `sudo apt install python3-pip`
               * `pip3 install praw` (https://praw.readthedocs.io/en/latest/)
               * `python3 RedditPostNotification.py`

# How to build the config file
Building the config...

# Todo
* search not only the title but also the content of the post
* if the repo is updated the program should prompt the user to update
* refactor code (clean up)

# Dependencies
1. Reddit account (free and doesn't require email)
2. Slack account (free)
3. Python v3.6+

# Resource Usage
Below is a screenshot of the resource usage of this application while running on Ubuntu Server 20.04.1 on a Raspberry Pi.

![Image of Usage](https://i.imgur.com/Satg3d1.png)
