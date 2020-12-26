import requests
from lxml import html

import time
import re

#############################################
#   Data structure for the pages to visit   #
#############################################

from collections import namedtuple

# Final values for the xpath to get the last table row value
XPATH_SAGATABLE_EPISODE_ROW = '//*[@class="sagatable"][1]//tr[2]'
XPATH_MEDIAITEM_EPISODE_ROW = '(//tr[@class="mediaitem"])[last()]'

XPATH_EPISODE_NUMBER = '/td[1]/text()'
XPATH_EPISODE_TITLE = '/td[2]/text()'

XPATH_MEDIAITEM_EPISODE_NUMBER = XPATH_MEDIAITEM_EPISODE_ROW + XPATH_EPISODE_NUMBER
XPATH_MEDIAITEM_EPISODE_TITLE = XPATH_MEDIAITEM_EPISODE_ROW + XPATH_EPISODE_TITLE
XPATH_MEDIAITEM_EPISODE_ONCLICK = XPATH_MEDIAITEM_EPISODE_ROW


XPATH_SAGATABLE_EPISODE_NUMBER = XPATH_SAGATABLE_EPISODE_ROW + XPATH_EPISODE_NUMBER
XPATH_SAGATABLE_EPISODE_TITLE = XPATH_SAGATABLE_EPISODE_ROW + XPATH_EPISODE_TITLE
XPATH_SAGATABLE_EPISODE_ONCLICK = XPATH_SAGATABLE_EPISODE_ROW + '//td[@onclick]'

# Data structure to hold scrape information per visited page
Page = namedtuple("Page", ["url", "xpath_episode_number","xpath_episode_title", "xpath_episode_onclick"])

# List of pages to scrape
pages_to_scrape = [
    Page(
        url="http://dragonball-tube.com/dragonball-super-episoden-streams",
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="http://dragonball-tube.com/dragonball-super-mangaliste",
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="http://dragonball-tube.com/galactic-patrol-mangaliste",
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="https://onepiece-tube.com/episoden-streams", 
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="https://onepiece-tube.com/kapitel-mangaliste", 
        xpath_episode_number=XPATH_SAGATABLE_EPISODE_NUMBER,
        xpath_episode_title=XPATH_SAGATABLE_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_SAGATABLE_EPISODE_ONCLICK),
    Page(
        url="http://fairytail-tube.org/episoden-streams", 
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="http://fairytail-tube.org/100-years-quest-mangaliste", 
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="http://fairytail-tube.org/edens-zero-mangaliste", 
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="http://naruto-tube.org/boruto-episoden-streams", 
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
    Page(
        url="http://naruto-tube.org/boruto-kapitel-mangaliste", 
        xpath_episode_number=XPATH_MEDIAITEM_EPISODE_NUMBER,
        xpath_episode_title=XPATH_MEDIAITEM_EPISODE_TITLE,
        xpath_episode_onclick=XPATH_MEDIAITEM_EPISODE_ONCLICK),
]

#############
#   Scraper #
#############

for page_to_scrape in pages_to_scrape:
    page = requests.get(page_to_scrape.url)
    tree = html.fromstring(page.content)
    episode_number = tree.xpath(page_to_scrape.xpath_episode_number)[0]
    episode_title = tree.xpath(page_to_scrape.xpath_episode_title)[0]
    episode_onclick = tree.xpath(page_to_scrape.xpath_episode_onclick)[0].attrib["onclick"]
    episode_path = re.match(r"window.location.href = '(.*)'", episode_onclick).group(1)
    episode_domain = re.match(r"(.*\/\/.*)\/", page_to_scrape.url).group(1)
    episode_url = episode_domain + episode_path
    time.sleep(5)
    print(f"[{episode_number}] {episode_title} -> {episode_url}")
    assert requests.get(episode_url).status_code == 200