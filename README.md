# RedditPostNotification
A program which will alert a user of of posts which are made in a specific subreddit if it matches specific search criteria. Depending on how many subreddits you are checking, a subreddit is queried at most once per second as per Reddit's API rules.

If this program works and saves you some money or time, consider sending me some BTC at `bc1qmqnmr8hwj2lcp2ccfg95k0378urfxtm80k7fu0` or my PayPal below. 

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WN85PYVLLLSKL&currency_code=USD)

# How to use
1. You need a reddit account (free, no email required) to get an application ID and secret in order to connect to the Reddit API (https://www.reddit.com/prefs/apps/)
2. You will a messaging app in order to be notified of the posts. If a messaging app you would like to use is not listed here, feel free to make a pull request. Please adhere as close as you can to the current layout of the config and program structure.
      * **Telegram** (recommended because it is easier to setup and doesn't use Google services to push notifications on Android)
          * update the config to use telegram as the notification app
          * in Telegram, create a bot using @BotFather (https://t.me/botfather)
          * add the token of your new bot (example token: `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`) to the config
          * in Telegram, add @userinfobot (https://t.me/userinfobot) and start a conversation to find your account id (must be included in the config on each filter that you want to be notified about)
      * **Slack**
          * update the config to use slack as the notification app
          * create a workspace, and a webhook in that workspace to send notifications (https://api.slack.com/messaging/webhooks)
          * if you want to be mentioned in the notification, add your slack id in the filters you would like to be mentioned in
4. Navigate to your home directory and clone the repo
      * `cd ~`
      * `git clone https://github.com/tcm5343/RedditPostNotification.git`
      * `cd RedditPostNotification`
5. Create `config.json` to store the credentials (refer to `example_config.json`) and place it in RedditPostNotification/
6. Modify the `config.json` to include subreddits and keyword filters which you want to be notified about
7. Run the script
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
TODO

# Dependencies
1. Reddit account (free and doesn't require email)
2. Notification App (Slack or Telegram)
3. Python v3.6+

# Resource Usage
Below is a screenshot of the resource usage of this application while running on Ubuntu Server 20.04.1 on a Raspberry Pi.

![Image of Usage](https://i.imgur.com/1MKmEzK.png)
