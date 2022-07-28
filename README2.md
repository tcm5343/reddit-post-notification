# reddit-post-notification
A program that you can self host which will alert a user of of posts which are made in a specific subreddit if it matches specific search criteria. Depending on how many subreddits you are checking, a subreddit is queried at most once per second as per Reddit's API rules.

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
      * `git clone https://github.com/tcm5343/reddit-post-notification.git`
      * `cd reddit-post-notification`
5. Create `config.json` to store the credentials (refer to `example_config.json`) and place it in RedditPostNotification/
6. Modify the `config.json` to include subreddits and keyword filters which you want to be notified about
7. Run the script
     * Using Docker (Docker must be installed)
          * `sudo docker build -t "redditpostnotification" ./`
          * `sudo docker run --restart unless-stopped --name redditapp -v ~/reddit-post-notification:/usr/src/app -d redditpostnotification`
     * Traditionaly
          * Windows
               * `pip install praw` (https://praw.readthedocs.io/en/latest/)
               * `python reddit_post_notification.py`
          * Linux
               * `sudo apt install python3-pip`
               * `pip3 install praw` (https://praw.readthedocs.io/en/latest/)
               * `python3 reddit_post_notification.py`

# How to build the config file
TODO: Add instructions on building config

`"__users__"`: Only used as a comment to store the user id's of the users of the program. This field is never accessed by the program.

`"reddit"`
- `"clientId"`
- `"clientSecret"`

`"notifications"`
- `"app"`: String which tells the program which notification app you are using. (only valid values are "slack" or "telegram")
- `"telegram"`
     - `"token"`
- `"slack"`
     - `"webhook-url"`

`"search"`

`"filters"`
- `"includes"`: Array of substrings that are all required to be in the post for a notification to be sent.
- `"except"`: Array of substrings that if any are in the post title, the notification will not be sent.
- `"notify"`: Array of strings containing the user id's for a notification to be sent to. (optional for Slack)

# Dependencies
1. Reddit account (free and doesn't require email)
2. Notification App (Slack or Telegram)
3. Python v3.6+

# FAQ
### If a post triggers multiple filters in a subreddit, will notifications be sent correctly?
- Yes, all filters within a subreddit are processed against a post title at the same time using multiprocessing. If whomever is set to be notified is on one or more of the filters which would trigger a notification, they will receive one notification for the post.

# Speed
Although this program is not resource heavy, the post's processing time is correlated to what hardware it is running on. For the test, there are two subreddits with the same amount of filters and each of them contain all of the attributes which were available at the time.

- **4-15-2021** - The average time taken from filtering 100 different posts is 0.283 seconds. (using Process)
- **4-16-2021** - The average time taken from filtering 100 different posts is 0.034 seconds. (using Thread)

After this point, the `have` and `want` attributes were added into the test.
- **4-24-2021** - The average time from filtering 50 different posts is .0387 seconds. (using Thread and refactored filter attribute handling)
- **4-24-2021** - The average time from filtering 50 different posts is .035 seconds. (Using Threads handling the filters attributes in a simple way)


# Resource Usage
Below is a screenshot of the resource usage of this application while running on Ubuntu Server 20.04.1 on a Raspberry Pi.

![Image of Usage](https://i.ibb.co/VxJVVtC/Screen-Shot-2021-04-11-at-9-50-08-PM.png)

# Dev
A pylintrc is already created and any pull requests must pass completely. To run pylint locally execute `pylint --rcfile=.pylintrc src/reddit_post_notification.py
`

coverage run -m pytest ./tests/  # to run unit tests and gather coverage
coverage report  # output coverage report
pylint ./src ./tests  # code formatting