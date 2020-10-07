# RedditPostNotification
A program which will alert a user of of posts which are made in a specific subreddit if it matches specific search criteria. Depending on how many subreddits you are checking, a subreddit is queried at most once per second as per Reddit's API rules.

If this program works and saves you some money, consider supporting me by buying me a coffee:

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WN85PYVLLLSKL&currency_code=USD)

# How to use
1. You need a reddit account (free, no email required) to get an application ID and secret in order to connect to the Reddit API (https://www.reddit.com/prefs/apps/)
2. You will need a slack account, create a workspace, and a webhook to send notifications (https://api.slack.com/messaging/webhooks)
3. Create a `config.json` file to store the credentials (refer to `example_config.json`)
4. Modify the `config.json` to include subreddits and keyword filters which you want to be notified about
5. Build and run the script
   * Windows
       * `git clone https://github.com/tcm5343/RedditPostNotification.git`
       * `cd RedditPostNotification`
       * `pip install praw` (https://praw.readthedocs.io/en/latest/)
       * `python app.py`
   * Linux
       * `git clone https://github.com/tcm5343/RedditPostNotification.git`
       * `cd RedditPostNotification`
       * `sudo apt install python-pip`
       * `pip3 install praw` (https://praw.readthedocs.io/en/latest/)
       * `python3 app.py`

# Todo
1. search not only the title but also the content of the post
2. add more functionality/options to config file
3. if the repo is updated the program should prompt the user to update
4. Add error messages and test
5. create thorough documentation when core functionality is complete
6. allow notication do be sent through discord
7. refactor code (clean up)
8. write errors to `error.log` instead of printing to screen
9. give output to user of what the current process is (in the terminal)

# Dependencies
1. Reddit account (free and doesn't require email)
2. Slack account (free)
3. Python v3.6+

# Resource Usage
![Image of Usage](https://i.imgur.com/2OkJes4.png)
