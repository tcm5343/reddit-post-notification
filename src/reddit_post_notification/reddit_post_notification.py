from time import time, sleep

import praw

from config.config import import_config
from post.process_post import process_submission


def main():
    config = import_config('./config.json')

    reddit = praw.Reddit(
        username=config["reddit"]["username"],
        password=config["reddit"]["password"],
        client_id=config["reddit"]["clientId"],
        client_secret=config["reddit"]["clientSecret"],
        user_agent="default",
    )

    subreddit_names = list(config["search"].keys())
    last_post_scanned = {str(subreddit_name): time() for subreddit_name in subreddit_names}
    number_of_posts = 0
    total_time = 0

    while True:
        for subreddit_name in subreddit_names:
            print("Processing", subreddit_name)
            latest_post_time = 0

            subreddit_posts = reddit.subreddit(subreddit_name).new(limit=5)
            for submission in subreddit_posts:
                # updates the time of the most recently filtered submission
                latest_post_time = submission.created_utc \
                    if submission.created_utc > latest_post_time else latest_post_time

                if submission.created_utc > last_post_scanned[subreddit_name]:
                    start = time()

                    last_post_scanned[subreddit_name] = submission.created_utc
                    process_submission(submission, subreddit_name, config)

                    total_time += time() - start
                    number_of_posts += 1

                    print("new average time for", number_of_posts, "submission(s):",
                          total_time / number_of_posts, '\n')
            sleep(2)


if __name__ == '__main__':
    main()
