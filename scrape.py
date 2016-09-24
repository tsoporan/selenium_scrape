from selenium import webdriver
from lxml import html

import time, os
import config

URL = config.URL
USER = config.USERNAME
PASS = config.PASSWORD
URLS_FILE = 'img_urls.txt'

# Set up a browser profile, javascript disabled
fp = webdriver.FirefoxProfile()
fp.set_preference("javascript.enabled", False)

browser = webdriver.Firefox(firefox_profile=fp)

# Navigates to page
browser.get(URL)

# Login via form
login_form = browser.find_element_by_id('loginform')
login_form.find_element_by_id('user_login').send_keys(USER)
login_form.find_element_by_id('user_pass').send_keys(PASS)
login_form.submit()

# Parse HTML
h = html.fromstring(browser.page_source)

# Example of extracting image urls
gallery_links = h.find_class('gallery_link')
gallery_urls = [l.attrib['href'] for l in gallery_links]

for url in gallery_urls:

    # Navigates to the gallery
    browser.get(url)

    h = html.fromstring(browser.page_source)

    # Find all image links in gallery
    imgs = [i.attrib['href'] for i in h.xpath('//div[@class="ngg-gallery-thumbnail"]/a')]

    # Append to file
    with open(URLS_FILE, 'a') as f:
        for j in imgs:
            f.write(j + '\n')

    # Wait a bit before navigations
    time.sleep(5)

# All done
browser.close()
