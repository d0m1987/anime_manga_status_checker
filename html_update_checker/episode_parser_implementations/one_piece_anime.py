from typing import List

from html_update_checker.episode import EpisodeParser

class OnePieceAnimeEpisodeParser(EpisodeParser):
    def parse_to_list_of_episodes(self, homepage:"Homepage") -> List["Episode"]:
        pass