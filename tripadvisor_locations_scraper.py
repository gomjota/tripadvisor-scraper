import logging
import time

from config.config import SECONDS_BETWEEN_REQUEST, I18N
from model.location import Location
from utils import get_language_by_url


class TripadvisorLocationsScraper:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def fetch_locations(self):
        print('Fetching locations...', flush=True)
        self.driver.get(self.url)
        has_next = True
        iterator_count = 0

        locations = []
        while has_next:
            if iterator_count > 0:
                location_elements = self.driver.find_element_by_xpath('//*[@id="LOCATION_LIST"]/ul')
                location_elements = location_elements.find_elements_by_tag_name('li')
            else:
                location_elements = self.driver.find_elements_by_class_name('geo_name')

            for e in location_elements:
                try:
                    url = e.find_element_by_tag_name('a').get_attribute('href')
                    url_text = e.find_element_by_tag_name('a').text
                    language = get_language_by_url(self.driver.current_url)
                    if language == 'es':
                        name = url_text.split(I18N[language]['in'] + ' ')[-1]
                    elif language == 'en':
                        name = url_text.split(' Restaurants')[0]
                    else:
                        name = ''
                    locations.append(Location(url, name))
                except:
                    logging.warning('Couldn\'t fetch location.')
                    pass

            if iterator_count > 0:
                next_page = ".pgLinks>.sprite-pageNext"
            else:
                next_page = ".pagination>.next"

            try:
                has_next = self.driver.execute_script(
                    'return !document.querySelector("' + next_page + '").classList.contains("disabled")')
                if has_next:
                    self.driver.execute_script(
                        'document.querySelector("' + next_page + '").click()')
            except:
                has_next = False

            iterator_count += 1
            time.sleep(SECONDS_BETWEEN_REQUEST)
        return locations
