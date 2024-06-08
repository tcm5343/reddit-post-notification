import re

from praw.models import Submission


class SubmissionFilter:
    def __init__(self, filter_name, filter_def):
        self.name = filter_name
        self.filter_parts = filter_def
        self.notify_def = filter_def.get("notify", {})

    def __eval_includes(self, part, target_string: str):
        if all([substring in target_string for substring in self.filter_parts[part].get('includes', [])]):
            return True
        return False

    def __eval_excludes(self, part, target_string: str):
        if any([substring in target_string for substring in self.filter_parts[part].get('excludes', [])]):
            return False
        return True

    def __eval_regex(self, part, target_string: str):
        if all([re.search(pattern, target_string) for pattern in self.filter_parts[part].get('regex', [])]):
            return True
        return False

    def eval(self, post: Submission) -> bool:
        """
        Evaluate a post to see if a notification should be sent.

        Criteria:
            1. All filters (include, exclude, ...) for a given part of a post (title, body, ...) must pass for truthy
            2. If any part is truthy, a message is sent
        """
        lowered_title = post.title.lower()
        string_parts = {  # todo: lazily evaluate this
            'have': post.title[lowered_title.find("[h]") + 3:lowered_title.find("[w]")],
            'want': post.title[lowered_title.find("[w]") + 3:],
            'title': post.title,
            'body': post.selftext,
            'post': post.title + " " + post.selftext,  # post is defined as both title and body
            'url': post.url,
        }
        for key, value in self.filter_parts.items():
            if key != 'notify':
                target_string = string_parts[key]
                includes = self.__eval_includes(key, target_string)
                excludes = self.__eval_excludes(key, target_string)
                regex = self.__eval_regex(key, target_string)
                if includes and excludes and regex:
                    return True
        return False
