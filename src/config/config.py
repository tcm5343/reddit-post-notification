from typing import Optional, List

from praw.models import Submission
import yaml

from notifiers.telegram_notifier import TelegramNotifier
from submission_filter.submission_filter import SubmissionFilter


class Config:
    def __init__(self, path):
        self.__read_config(path)
        self.__configure_notifiers()

    def get_filter_def_by_name(self, filter_name: str) -> Optional[SubmissionFilter]:
        filter_def = self.config.get('filters', {}).get(filter_name)
        if filter_def:
            return SubmissionFilter(filter_name, filter_def)
        return None

    def get_filter_def_by_names(self, filter_names: list[str]) -> List[SubmissionFilter]:
        if filter_names:
            return [self.get_filter_def_by_name(filter_name) for filter_name in filter_names
                    if self.get_filter_def_by_name(filter_name)]
        return []

    def __configure_notifiers(self):
        self.notifiers = {}
        notifiers = self.config['creds'].get("notifiers")
        for service in notifiers:
            if service == 'telegram':
                self.notifiers[service] = TelegramNotifier(self.config['creds']['notifiers'][service].get('token'))

    def __get_universal_filters(self) -> List[SubmissionFilter]:
        universal_filter_names = self.config.get('search', {}).get('universal')
        if universal_filter_names:
            return self.get_filter_def_by_names(universal_filter_names)
        return []

    def __read_config(self, path: str):
        with open(path, encoding='utf-8') as config_file:
            self.config = yaml.safe_load(config_file)

    def get_subreddits(self):
        """
        subreddits key does not exist
        subreddits key is empty
        subreddits value is None
        subreddits returns expected
        """
        if self.config.get('search') and self.config['search'].get('subreddits'):
            return list(self.config['search']['subreddits'].keys())
        return None

    def __get_user_ids(self, service, aliases):
        service_user_ids = self.config.get('who').get(service)
        return [service_user_ids[alias] for alias in aliases if alias in service_user_ids]

    def get_filters(self, subreddit: str) -> List[SubmissionFilter]:
        """
        no universal key
        universal value is empty
        universal value is None
        universal value is set
        subreddit_name value is None
        subreddit_name value is empty
        subreddit_name value is set
        both subreddit_name and universal value set
        """
        if self.config.get('search') and self.config['search'].get('subreddits'):
            filter_names = self.config['search']['subreddits'].get(subreddit)
            return self.get_filter_def_by_names(filter_names) + self.__get_universal_filters()
        return []

    def notify(self, notify_def, submission: Submission):
        for service, user_aliases in notify_def.items():
            self.notifiers[service].send(submission, self.__get_user_ids(service, user_aliases))
