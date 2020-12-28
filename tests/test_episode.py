import pytest 
from typing import List

from html_update_checker.episode import Episode, EpisodeParser

class TestEpisode:

    def test_episode_object_creation(self):
        name = "TestEpisode"
        url = "https://www.test.com"
        episode_number = 123
        episode = Episode(name, url, episode_number)
    
    def test_greater_than_between_two_episodes(self):
        name = "TestEpisode"
        url = "https://www.test.com"
        episode_1 = Episode(name, url, 123)
        episode_2 = Episode(name, url, 1337)

        assert (episode_1 > episode_2) == False

    def test_equals_between_two_episodes(self):
        name = "TestEpisode"
        url = "https://www.test.com"
        episode_1 = Episode(name, url, 123)
        episode_2 = Episode(name, url, 123)

        assert (episode_1 == episode_2) == True
        episode_1.episode_number = 124
        assert (episode_1 == episode_2) == False

class EpisodeParserForTests(EpisodeParser):
    def parse_to_list_of_episodes(self, homepage:"Homepage") -> List["Episode"]:
        return [Episode("test1","https://www.google.com",1), Episode("test2","https://www.google.com",2)]

class TestEpisodeParser:

    def test_missing_abstract_method_raises_error(self):
        class EpisodeParser_Test(EpisodeParser):
            pass

        with pytest.raises(TypeError):
            episode_parser = EpisodeParser_Test()