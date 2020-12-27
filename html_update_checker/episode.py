from abc import ABC, abstractmethod
from typing import List

class Episode:
    def __init__(self, name:str, url:str, episode_number:int):
        self.name = name
        self.url = url
        self.episode_number = episode_number
    
    def __gt__(self, other:"Episode") -> bool:
        return self.episode_number > other.episode_number

class EpisodeParser(ABC):
    episode_parsers = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.episodes = list()
        EpisodeParser.episode_parsers[cls.__name__] = cls
    
    @abstractmethod
    def parse_to_list_of_episodes(self, homepage:"Homepage") -> List["Episode"]:
        pass
