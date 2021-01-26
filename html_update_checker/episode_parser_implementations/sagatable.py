from typing import List
import requests
from lxml import html
import re
import funcy

from html_update_checker.episode import (
    EpisodeParser,
    Episode)
class SagatableEpisodeParser(EpisodeParser):
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
        XPATH_SAGATABLE_EPISODE_ROW = '//*[@class="sagatable"][1]//tr'
        XPATH_EPISODE_NUMBER = './td[1]/text()'
        XPATH_EPISODE_TITLE = './td[2]/text()'
        
        episodes = []
        tree = html.fromstring(html_code)
        sagatable_items = tree.xpath(f'{XPATH_SAGATABLE_EPISODE_ROW}')
        # Remove header with "Nr. | <Name of arc> | Seiten | Release"
        sagatable_items = sagatable_items[1:]
        
        for sagatable_item in sagatable_items:
            episode_number = sagatable_item.xpath(f'{XPATH_EPISODE_NUMBER}')[0]
            episode_title = sagatable_item.xpath(f'{XPATH_EPISODE_TITLE}')[0]
            episode_onclick = sagatable_item.xpath('//td[@onclick]')[0].attrib["onclick"]
            episode_path = re.match(r"window.location.href = '(.*)'", episode_onclick).group(1)
            episode_domain = re.match(r"(.*\/\/.*)\/", url).group(1)
            episode_url = episode_domain + episode_path
            episodes.append(Episode(episode_title, episode_url, int(episode_number)))

        return episodes