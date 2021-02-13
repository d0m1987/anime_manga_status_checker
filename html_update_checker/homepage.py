from abc import abstractmethod
import logging
from typing import List
class Homepage:
    homepages = dict()

    def __init__(self, url, episode_parser: "EpisodeParser", name=None):
        self.name = name or url
        self.url = url
        self.users_to_notify = dict()
        self._episode_parser = episode_parser
        self._episodes = self._episode_parser().parse_to_list_of_episodes(self)
        Homepage.homepages[self.url] = self

    def __identify_new_episodes(self, old_episodes:List["Episode"], new_episodes:List["Episode"]) -> List["Episode"]:
        diff_episodes = []

        # Prevents "not iterable" error if no new_episodes exist
        if not new_episodes: return []
        
        for episode in new_episodes:
            if episode not in old_episodes:
                diff_episodes.append(episode)
        
        return diff_episodes
    
    def __update_users_about_new_episodes(self, episodes:List["Episode"]) -> None:
        for user in self.users_to_notify.values():
            for episode in episodes:
                user.add_update_notification(self, episode)

    def episodes_update(self) -> None:
        """
        Gets the current episodes, compares it with the current episodes and
        notifies the users that want to get notified. Then sets the Homepage objects
        episodes to the episodes that are currently available.
        """
        # Get currently available episodes in extra variable
        episodes = self._episode_parser().parse_to_list_of_episodes(self)

        # Calculate the episodes that are new
        new_episodes = self.__identify_new_episodes(self._episodes, episodes)

        # Give update on new episodes to users that want to be informed
        self.__update_users_about_new_episodes(new_episodes)

        # Update self._episodes with the most recent episodes
        self._episodes = episodes

        # Log update
        if new_episodes:
            logging.info(f"Successfully updated homepage {self.url}. Found {len(new_episodes)} new episodes.")

    def register_for_updates(self, user:"User") -> None:
        self.users_to_notify[user.email] = user
        logging.info(f"[{user.email}] Registered {self.url}")
    
    def unregister_for_updates(self, user:"User") -> None:
        del self.users_to_notify[user.email]
        logging.info(f"[{user.email}] Unregistered {self.url}")


class HomepageUpdateInterface:
    @abstractmethod
    def add_update_notification(homepage: "Homepage", episode: "Episode") -> None:
        pass 