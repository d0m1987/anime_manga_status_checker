from abc import ABC, abstractmethod
from typing import List

class Episode:
    def __init__(self, name:str, url:str, episode_number:int):
        self.name = name
        self.url = url
        self.episode_number = episode_number
    
    def __str__(self) -> str:
        return f"[{self.episode_number}] {self.name} (Link: {self.url})"
    
    def __repr__(self) -> str:
        return f"[{self.episode_number}] {self.name} (Link: {self.url})"

    def __gt__(self, other:"Episode") -> bool:
        return self.episode_number > other.episode_number

    def __eq__(self, other) -> bool:
        if not isinstance(other, Episode):
            return False
        if (self.name == other.name) and (self.url == other.url) and (self.episode_number == other.episode_number):
            return True
        
        return False
class EpisodeParser(ABC):
    episode_parsers = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.episodes = list()
        EpisodeParser.episode_parsers[cls.__name__] = cls
    
    @abstractmethod
    def parse_to_list_of_episodes(self, homepage:"Homepage") -> List["Episode"]:
        pass
