import logging
import time

from config.config import SECONDS_BETWEEN_REQUEST


class TripadvisorRestaurantsScraper:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def fetch_restaurants(self):
        print('Fetching restaurants...', flush=True)
        self.driver.get(self.url)
        has_next = True
        iterator_count = 0

        restaurants = []
        while has_next:
            try:
                restaurant_elements = self.driver.find_element_by_id('EATERY_SEARCH_RESULTS').find_elements_by_class_name('listing')
            except:
                time.sleep(SECONDS_BETWEEN_REQUEST)
                continue

            for e in restaurant_elements:
                try:
                    url = e.find_element_by_class_name('title').find_element_by_tag_name('a').get_attribute('href')
                    if url:
                        print(url)
                        restaurants.append(url)
                except:
                    print('[ERROR] fetching restaurants with url: ' + self.url, flush=True)
                    pass


            try:
                has_next = self.driver.execute_script(
                    'return !document.querySelector(".pagination>.next").classList.contains("disabled")')
            except:
                has_next = False

            if has_next:
                self.driver.execute_script(
                    'document.querySelector(".pagination>.next").click()')

            iterator_count += 1
            time.sleep(SECONDS_BETWEEN_REQUEST)
        return restaurants
