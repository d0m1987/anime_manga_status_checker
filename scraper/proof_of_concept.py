import time

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
    Page("http://dragonball-tube.com/dragonball-super-episoden-streams",XPATH_MEDIAITEM),
    Page("http://dragonball-tube.com/dragonball-super-mangaliste",XPATH_MEDIAITEM),
    Page("http://dragonball-tube.com/galactic-patrol-mangaliste",XPATH_MEDIAITEM),
    Page("https://onepiece-tube.com/episoden-streams", XPATH_MEDIAITEM),
    Page("https://onepiece-tube.com/kapitel-mangaliste", XPATH_SAGATABLE),
    Page("http://fairytail-tube.org/episoden-streams", XPATH_MEDIAITEM),
    Page("http://fairytail-tube.org/100-years-quest-mangaliste", XPATH_MEDIAITEM),
    Page("http://fairytail-tube.org/edens-zero-mangaliste", XPATH_MEDIAITEM),
    Page("http://naruto-tube.org/boruto-episoden-streams", XPATH_MEDIAITEM),
    Page("http://naruto-tube.org/boruto-kapitel-mangaliste", XPATH_MEDIAITEM),
]

#############
#   Scraper #
#############

driver = webdriver.Chrome()
driver.implicitly_wait(15)

for page in pages_to_scrape:
    driver.get(page.url)
    # If the element can't be found, we assume that there is a data protection notice that needs to be closed.
    element = driver.find_element_by_xpath(page.xpath)
    if not element.text:
        # Closing the data protection notice and trying again to find the element
        iframe = driver.find_element_by_xpath('//*[contains(@id,"sp_message_iframe")]')
        driver.switch_to.frame(iframe)
        driver.find_element_by_xpath('//button[@title="Accept and close"]').click()
        driver.switch_to.default_content()
        element = driver.find_element_by_xpath(page.xpath)
    print(element.text)
    time.sleep(5)

driver.close()