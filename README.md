# reddit-post-notification
A CLI tool written in Python to alert a user of posts made on Reddit.

This tool is open source and [V4V](https://value4value.info/). If you get value, consider returning some value by contributing to the codebase or 
sending me some value through BTC at `bc1qmqnmr8hwj2lcp2ccfg95k0378urfxtm80k7fu0` or PayPal below.

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WN85PYVLLLSKL&currency_code=USD)

# How to use
1. You need a Reddit account to get a client ID and secret to connect to the [Reddit API](https://www.reddit.com/prefs/apps/)
2. Notifications are sent via messaging apps.
      * **Telegram** (recommended because it is easier to setup and doesn't use Google services to push notifications on Android)
          * update the config to use telegram as the notification app
          * in Telegram, create a bot using [@BotFather](https://t.me/botfather)
          * add the token of your new bot (example token: `110201543:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw`) to the config
          * in Telegram, add [@userinfobot](https://t.me/userinfobot) and start a conversation to find your account id 
          (must be included in the config on each filter that you want to be notified about)

[//]: # (      * **Slack &#40;TBD&#41;**)

[//]: # (          * update the config to use slack as the notification app)

[//]: # (          * create a workspace, and a webhook in that workspace to send notifications &#40;https://api.slack.com/messaging/webhooks&#41;)

[//]: # (          * if you want to be mentioned in the notification, add your slack id in the filters you would like to be mentioned in)

# Running the Program
TODO

# How to build the config file
TODO

# Dependencies
1. Reddit account (free and doesn't require email)
2. Notification App (Slack or Telegram)
3. Python v3.10+

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
