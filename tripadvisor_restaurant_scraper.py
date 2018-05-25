import json

from config.config import I18N, PRICE, RATING
from model.address import Address
from model.rating import Rating
from model.restaurant import Restaurant
from utils import get_id_by_url, get_language_by_url


class TripadvisorRestaurantScraper:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def __obj_dict(self, obj):
        return obj.__dict__

    def fetch_restaurant(self):
        self.driver.get(self.url)
        _id = get_id_by_url(self.url)

        print('Fetching restaurant with id: ' + _id, flush=True)
        name = self.driver.find_element_by_class_name('heading_title').text

        try:
            total_rating = float(
                self.driver.find_element_by_class_name('ui_bubble_rating').get_attribute('content').replace(',', '.'))
        except:
            total_rating = -1

        try:
            ranking_position = int(self.driver.find_element_by_class_name('header_popularity').find_element_by_tag_name(
                'b').find_element_by_tag_name('span').text.split('º ')[-1].split('#')[1].replace(',', ''))
        except:
            ranking_position = -1

        try:
            price = PRICE[get_language_by_url(self.driver.current_url)][
                self.driver.find_element_by_class_name('header_tags').text.replace(' ', '')]
        except:
            price = -1

        try:
            tags = self.driver.find_element_by_class_name('header_links').text.split(', ')
        except:
            tags = ""

        try:
            street_address = self.driver.find_element_by_class_name('street-address').text
        except:
            street_address = ""

        try:
            locality_address = self.driver.find_element_by_class_name('locality').text
        except:
            locality_address = ""

        try:
            country_address = self.driver.find_element_by_class_name('country-name').text
        except:
            country_address = ""

        try:
            phone = self.driver.find_element_by_class_name('phone').text
        except:
            phone = ""

        try:
            cuisines = self.driver.find_element_by_xpath(
                '//*[@id="taplc_restaurants_detail_info_content_0"]/div[2]/div/div[2]/div[2]').get_attribute(
                'data-content').replace(', ', ',').split(',')
        except:
            cuisines = ""

        address = Address(street_address, locality_address, country_address)

        ratings = []
        for i in range(2, 6):
            try:
                rating_element = self.driver.find_element_by_xpath(
                    '//*[@id="taplc_restaurants_detail_info_content_0"]/div[3]/div[' + str(
                        i) + ']')
            except:
                rating_element = None

            if rating_element:
                rating_name = rating_element.text
                try:
                    rating_value = RATING[rating_element.find_element_by_class_name(
                        'ui_bubble_rating').get_attribute('class').split(' ')[-1]]
                except:
                    rating_value = -1
                rating = Rating(rating_name, rating_value)
                ratings.append(rating)

        restaurant = Restaurant(_id, name, total_rating, ranking_position, price, tags, address, phone, cuisines,
                                ratings)
        print('[COMPLETED]', flush=True)
        return restaurant.to_dict()
