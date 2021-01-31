from typing import List
import requests
from lxml import html
import funcy

from html_update_checker.episode import (
    EpisodeParser,
    Episode)

class ReadDragonballSuperEpisodeParser(EpisodeParser):
    def parse_to_list_of_episodes(self, homepage:"Homepage") -> List["Episode"]:
        # Get HTML code of requested site
        html_code = self.__get_html_code(homepage.url)
        # Parse HTML code to separate episodes
        return self.__parse_episodes(html_code, homepage.url)
    
    @funcy.retry(3)
    def __get_html_code(self, url:str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    
    def __parse_episodes(self, html_code:str, url:str) -> List["Episode"]:
        XPATH_EPISODES = '//*[@id="Chapters_List"]/ul/li/ul/li/a'
        
        episodes = []
        tree = html.fromstring(html_code)
        media_items = tree.xpath(f'{XPATH_EPISODES}')

        for media_item in media_items:
            episode_number = media_item.text.split(" ")[-1]
            episode_title = media_item.text
            episode_url = media_item.attrib["href"]
            episodes.append(Episode(episode_title, episode_url, int(episode_number)))

        return episodes