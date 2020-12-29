from typing import List

from html_update_checker.homepage import Homepage
from html_update_checker.episode import EpisodeParser, Episode

class TestHomepage:

    def test_homepage_object_creation(self):
        class TestEpisodeParser(EpisodeParser):
            def parse_to_list_of_episodes(self, homepage:"Homepage") -> List["Episode"]:
                pass
        
        url = "https://www.test.com"
        episode_parser = TestEpisodeParser
        homepage = Homepage(url, episode_parser=episode_parser, name="Test")

    def test_identify_new_episodes(self):
        name = "TestEpisode"
        url = "https://www.test.com"

        episode_1 = Episode(name, url, 123)
        episode_2 = Episode(name, url, 124)
        episode_3 = Episode(name, url, 125)

        old_episodes = [episode_2, episode_1]
        new_episodes = [episode_1, episode_2, episode_3] 
        diff_episodes = [episode_3]

        calculated_diff_episodes = Homepage._Homepage__identify_new_episodes(None, old_episodes, new_episodes)

        assert calculated_diff_episodes == diff_episodes