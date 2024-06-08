from copy import deepcopy
from multiprocessing import Queue
from threading import Thread

from praw.models import Submission

from config.config import Config
from submission_filter.submission_filter import SubmissionFilter


def __filter_post(post: Submission, submission_filter: SubmissionFilter, queue: Queue):
    queue_dict = queue.get()
    queue_dict["notify"] = submission_filter.eval(post)
    if queue_dict["notify"]:
        queue_dict["notify_def"] = submission_filter.notify_def
    queue.put(queue_dict)


def process_submission(submission: Submission, subreddit_name: str, config: Config):
    queue = Queue()
    submission_filters = config.get_filters(subreddit_name)

    threads = []
    return_vals = {
        "notify": False,
        "notify_def": {}
    }

    for i, submission_filter in enumerate(submission_filters):
        ret = deepcopy(return_vals)
        queue.put(ret)

        thread = Thread(
            target=__filter_post,
            args=(submission, submission_filter, queue)
        )
        threads.append(thread)
        threads[i].start()

    # when a thread is finished, a record is pulled off the queue and processed
    for thread in threads:
        thread.join()
        ret = queue.get()

        if ret["notify"]:
            return_vals["notify"] = True
            for service in ret["notify_def"]:
                return_vals["notify_def"][service] = (
                        return_vals["notify_def"].get(service, []) + ret["notify_def"][service]
                )

    if return_vals["notify"]:
        return_vals["notify_def"] = {
            service: list(set(who_to_notify)) for service, who_to_notify in return_vals['notify_def'].items()
        }
        config.notify(return_vals["notify_def"], submission)
