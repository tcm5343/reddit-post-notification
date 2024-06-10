import re

from praw.models import Submission


# pylint: disable=too-few-public-methods
class SubmissionFilter:
    def __init__(self, filter_name, filter_def):
        self.name = filter_name
        self.filters = filter_def
        self.notify_def = filter_def.get('notify', {})
        self.valid_filter_rules = ['includes', 'excludes', 'regex']
        self.valid_part_of_post = ['title', 'body', 'have', 'want', 'post', 'url']

    def __eval_includes(self, part, target_string: str):
        checks = self.filters[part].get('includes', [])
        if not checks:
            return True
        for check in checks:
            if all(substring in target_string for substring in check):
                return True
        return False

    def __eval_excludes(self, part, target_string: str):
        """
        returns truthy if every substring in a given check are not in the target_string for each check
        """
        checks = self.filters[part].get('excludes', [])
        if not checks:
            return True
        for check in checks:
            if any(substring in target_string for substring in check):
                return False
        return True

    def __eval_regex(self, part, target_string: str):
        checks = self.filters[part].get('regex', [])
        if not checks:
            return True
        for check in checks:
            if all(re.search(pattern, target_string) for pattern in check):
                return True
        return False

    def eval(self, post: Submission) -> bool:
        """
        Evaluate a post to see if a notification should be sent.

        Criteria:
            1. Any filter (includes, excludes, ...) for a given part of a post (title, body, ...) must pass for truthy
                for includes and exlcudes: all elements of a filter must be present in the target string
            2. If any part is truthy, a message is sent
        """
        if not [part_of_post in self.valid_part_of_post for part_of_post in self.filters]:
            return False

        lowered_title = post.title.lower()
        string_parts = {
            'have': lambda: post.title[lowered_title.find('[h]') + 3:lowered_title.find('[w]')],
            'want': lambda: post.title[lowered_title.find('[w]') + 3:],
            'title': lambda: post.title,
            'body': lambda: post.selftext,
            'post': lambda: post.title + ' ' + post.selftext,  # post is defined as both title and body
            'url': lambda: post.url,
        }
        for part_of_post in self.filters:
            if part_of_post in self.valid_part_of_post:
                target_string = string_parts[part_of_post]()
                includes = self.__eval_includes(part_of_post, target_string)
                excludes = self.__eval_excludes(part_of_post, target_string)
                regex = self.__eval_regex(part_of_post, target_string)
                if includes and excludes and regex:
                    return True
        return False
