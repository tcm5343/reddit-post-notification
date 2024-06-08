from time import time, sleep

from praw import Reddit

from post.process_post import process_submission
from config.config import Config


def main():
    config = Config('./config.yml')

    reddit = Reddit(
        username=config.config['creds']["reddit"]["username"],
        password=config.config['creds']["reddit"]["password"],
        client_id=config.config['creds']["reddit"]["client_id"],
        client_secret=config.config['creds']["reddit"]["client_secret"],
        user_agent="default",
    )

    subreddit_names = config.get_subreddits()
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
