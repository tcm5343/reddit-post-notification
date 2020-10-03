# RedditPostNotification
A program which will alert a user of of posts which are made in a specific subreddit if it matches specific search criteria. Depending on how many subreddits you are checking, a subreddit is queried at most once per second as per Reddit's API rules.

<form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
<input type="hidden" name="cmd" value="_donations" />
<input type="hidden" name="business" value="WN85PYVLLLSKL" />
<input type="hidden" name="currency_code" value="USD" />
<input type="image" src="https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif" border="0" name="submit" title="PayPal - The safer, easier way to pay online!" alt="Donate with PayPal button" />
<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" />
</form>


# How to use
1. You need a reddit account (free, no email required) to get an application ID and secret in order to connect to the Reddit API (https://www.reddit.com/prefs/apps/)
2. You will need a slack account, create a workspace, and a webhook to send notifications (https://api.slack.com/messaging/webhooks)
3. Create a `config.json` file to store the credentials (refer to `example_config.json`)
4. Modify the `config.json` to include subreddits and keyword filters which you want to be notified about
5. Build and run the script
   * Windows
       * `git clone https://github.com/tcm5343/RedditPostNotification.git`
       * `cd RedditPostNotification`
       * `pip install praw`
       * `python app.py`
   * Linux (Mint)
       * `git clone https://github.com/tcm5343/RedditPostNotification.git`
       * `cd RedditPostNotification`
       * `pip3 install praw`
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

# Resource Usage
![Image of Usage](https://i.imgur.com/2OkJes4.png)
