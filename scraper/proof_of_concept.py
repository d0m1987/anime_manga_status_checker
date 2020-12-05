from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

#############################################
#   Data structure for the pages to visit   #
#############################################

from collections import namedtuple

# Final values for the xpath to get the last table row value
XPATH_SAGATABLE = '//*[@class="sagatable"][last()]//tr[last()]'
XPATH_MEDIAITEM = '(//tr[@class="mediaitem"])[last()]'

# Data structure to hold scrape information per visited page
Page = namedtuple("Page", ["url", "xpath"])

# List of pages to scrape
pages_to_scrape = [
    Page(
        "http://dragonball-tube.com/dragonball-super-episoden-streams", XPATH_MEDIAITEM
    ),
    Page("http://dragonball-tube.com/dragonball-super-mangaliste", XPATH_MEDIAITEM),
    Page("http://dragonball-tube.com/galactic-patrol-mangaliste", XPATH_MEDIAITEM),
]

#############
#   Scraper #
#############

driver = webdriver.Chrome()
driver.implicitly_wait(15)

for page in pages_to_scrape:
    driver.get(page.url)
    element = driver.find_element_by_xpath(page.xpath)
    print(element.text)

driver.close()