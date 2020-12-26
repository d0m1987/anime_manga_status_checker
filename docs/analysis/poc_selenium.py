import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from parse import *

#############################################
#   Data structure for the pages to visit   #
#############################################

from collections import namedtuple

# Final values for the xpath to get the last table row value
XPATH_FIRST_SAGATABLE_SECOND_TR = '//*[@class="sagatable"][1]//tr[2]'
XPATH_LAST_MEDIAITEM_TR = '(//tr[@class="mediaitem"])[last()]'

# Data structure to hold scrape information per visited page
Page = namedtuple("Page", ["url", "xpath"])

# List of pages to scrape
pages_to_scrape = [
    Page("http://dragonball-tube.com/dragonball-super-episoden-streams",XPATH_LAST_MEDIAITEM_TR),
    Page("http://dragonball-tube.com/dragonball-super-mangaliste",XPATH_LAST_MEDIAITEM_TR),
    Page("http://dragonball-tube.com/galactic-patrol-mangaliste",XPATH_LAST_MEDIAITEM_TR),
    Page("https://onepiece-tube.com/episoden-streams", XPATH_LAST_MEDIAITEM_TR),
    Page("https://onepiece-tube.com/kapitel-mangaliste", XPATH_FIRST_SAGATABLE_SECOND_TR),
    Page("http://fairytail-tube.org/episoden-streams", XPATH_LAST_MEDIAITEM_TR),
    Page("http://fairytail-tube.org/100-years-quest-mangaliste", XPATH_LAST_MEDIAITEM_TR),
    Page("http://fairytail-tube.org/edens-zero-mangaliste", XPATH_LAST_MEDIAITEM_TR),
    Page("http://naruto-tube.org/boruto-episoden-streams", XPATH_LAST_MEDIAITEM_TR),
    Page("http://naruto-tube.org/boruto-kapitel-mangaliste", XPATH_LAST_MEDIAITEM_TR),
]

#############
#   Scraper #
#############

driver = webdriver.Chrome()
driver.implicitly_wait(15)

for page in pages_to_scrape:
    driver.get(page.url)
    time.sleep(5)
    # If the element can't be found, we assume that there is a data protection notice that needs to be closed.
    element = driver.find_element_by_xpath(page.xpath)
    if not element.text:
        # Closing the data protection notice and trying again to find the element
        iframe = driver.find_element_by_xpath('//*[contains(@id,"sp_message_iframe")]')
        driver.switch_to.frame(iframe)
        driver.find_element_by_xpath('//button[@title="Accept and close"]').click()
        driver.switch_to.default_content()
        element = driver.find_element_by_xpath(page.xpath)
    element_tds = element.find_elements_by_tag_name("td")
    episode_number = element_tds[0].text
    episode_name = element_tds[1].text
    onclick = element.get_attribute("onclick") or element.find_element_by_xpath("//td[@onclick]").get_attribute("onclick")
    href_onclick = parse("window.location.href = '{}'", onclick)[0]
    href_window = driver.execute_script("return window.location.href")
    episode_href = f"{href_window}{href_onclick}"
    print(f"[{episode_number}] {episode_name} -> {episode_href}")

driver.close()