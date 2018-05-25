import argparse
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config.config import DEFAULT_LANGUAGE
from db.db import create_session, insert_restaurant_data, insert_reviews_data, restaurant_already_exists
from tripadvisor_locations_scraper import TripadvisorLocationsScraper
from tripadvisor_restaurant_scraper import TripadvisorRestaurantScraper
from tripadvisor_restaurants_scraper import TripadvisorRestaurantsScraper
from tripadvisor_reviews_scraper import TripadvisorReviewScraper
from utils import get_id_by_url


class TripadvisorScraper:
    def __init__(self):
        self.language = DEFAULT_LANGUAGE
        self.__init_webdriver()

    def __init_webdriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver')


    def get_driver(self):
        return self.driver

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description='Scrape restaurant reviews from Tripadvisor')
    #args = parser.parse_args()

    db = create_session()
    scraper = TripadvisorScraper()
    driver = scraper.get_driver()

    filepath = './data/locations.txt'
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            restaurants_scraper = TripadvisorRestaurantsScraper(driver, line)
            restaurants_urls = restaurants_scraper.fetch_restaurants()
            for restaurant_url in restaurants_urls:
                restaurant_scraper = TripadvisorRestaurantScraper(driver, restaurant_url)
                restaurant = restaurant_scraper.fetch_restaurant()
                if restaurant:
                    insert_restaurant_data(db, restaurant)
                review_scraper = TripadvisorReviewScraper(db, driver, restaurant_url)
                reviews = review_scraper.fetch_reviews()
                if reviews:
                    insert_reviews_data(db, reviews)
            line = fp.readline()

    scraper.close()
