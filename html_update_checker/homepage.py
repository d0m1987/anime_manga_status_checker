from abc import abstractmethod
from typing import List, Union, TYPE_CHECKING

from html_update_checker.episode import EpisodeParser, Episode
if TYPE_CHECKING:
    from html_update_checker.user import User

class Homepage:
    homepages = dict()

    def __init__(self, url, episodes_parser: EpisodeParser, name=None):
        self.name = name or url
        self.url = url
        self.users_to_notify = dict()
        self._episodes_parser = episodes_parser
        self._episodes = self._episodes_parser().parse_to_list_of_episodes(self)
        Homepage.homepages[self.url] = self

    def episodes_update(self) -> None:
        """
        Gets the current episodes, compares it with the current episodes and
        notifies the users that want to get notified. Then sets the Homepage objects
        episodes to the episodes that are currently available.
        """
        pass

    def register_for_updates(self, user:"User") -> None:
        self.users_to_notify[user.email] = user
    
    def unregister_for_updates(self, user:"User") -> None:
        del self.users_to_notify[user.email]


class HomepageUpdateInterface:
    @abstractmethod
    def add_update_notification(homepage: Homepage, episode: Episode) -> None:
        pass 