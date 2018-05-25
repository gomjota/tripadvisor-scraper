import datetime
import locale
import logging
import sys
import time
import pandas as pd
from langdetect import detect

from config.config import I18N, SECONDS_BETWEEN_REQUEST, RATING
from db.db import review_already_exists
from model.review import Review
from utils import get_language_by_url, is_valid_url, set_locale, get_id_by_url


class TripadvisorReviewScraper:
    def __init__(self, db, driver, url):
        self.db = db
        self.driver = driver
        self.lookup = {}
        self.url = url

    def __parse_page(self):
        try:
            self.driver.find_element_by_xpath('//span[contains(., "{}") and @class="taLnk ulBlueLinks"]'.format(
                I18N[get_language_by_url(self.url)]['more_btn'])).click()
            time.sleep(SECONDS_BETWEEN_REQUEST)
        except:
            pass

        try:
            more_button = self.driver.find_element_by_class_name('partial_entry').find_element_by_class_name('taLnk')
            if 'Expand' in more_button.get_attribute('onclick'):
                more_button.click()
                time.sleep(SECONDS_BETWEEN_REQUEST)
        except:
            pass

        reviews = self.__get_data([], [])
        return reviews

    def __get_data(self, ids_ready, reviews):
        review_elements = self.driver.find_elements_by_class_name('reviewSelector')
        for e in review_elements:
            try:
                _id = e.get_attribute('id')

                if review_already_exists(self.db, _id):
                    break

                if _id not in ids_ready:
                    set_locale(self.driver.current_url)
                    restaurant_id = get_id_by_url(self.driver.current_url)
                    date = e.find_element_by_class_name('ratingDate').get_attribute('title')
                    date = datetime.datetime.strptime(date,
                                                      I18N[get_language_by_url(self.driver.current_url)]['date_format'])
                    title = e.find_element_by_class_name('quote').find_element_by_tag_name(
                        'a').find_element_by_class_name(
                        'noQuotes').text
                    rating = RATING[
                        e.find_element_by_xpath(
                            '//*[@id="' + _id + '"]/div/div[2]/div/div[1]/div[1]/span[1]').get_attribute(
                            "class").split(' ')[1]]

                    try:
                        e.find_element_by_class_name('viaMobile')
                        via_mobile = True
                    except:
                        via_mobile = False

                    username = e.find_element_by_class_name('scrname').text

                    try:
                        more_button = e.find_element_by_class_name('taLnk')
                        if 'Expand' in more_button.get_attribute('onclick'):
                            more_button.click()
                            time.sleep(SECONDS_BETWEEN_REQUEST)
                    except:
                        pass

                    text = e.find_element_by_class_name('partial_entry').text.replace('\n', '')
                    language = detect(text)
                    ids_ready.append(_id)
                    reviews.append(
                        Review(_id, restaurant_id, date, title, username, text, rating, via_mobile, language))

                    self.__get_data(ids_ready, reviews)
                    break

            except:
                pass
        return reviews

    def fetch_reviews(self):
        print('Fetching reviews...', flush=True)
        self.lookup = {}
        reviews = []
        has_next = True
        set_locale(self.url)

        if not is_valid_url(self.url):
            print('[ERROR] URL is not valid: ' + self.url, flush=True)
            return None

        self.driver.get(self.url)

        try:
            self.driver.find_element_by_id('taplc_location_review_filter_controls_0_filterLang_ALL').click()
        except:
            pass

        while has_next:
            time.sleep(SECONDS_BETWEEN_REQUEST + 0.5)
            reviews_parsed = self.__parse_page()
            if len(reviews_parsed) == 0:
                break
            reviews += reviews_parsed
            print('Fetched reviews: ' + str(len(reviews)), flush=True)

            try:
                has_next = self.driver.execute_script(
                    'return !document.querySelector(".ui_pagination>.next").classList.contains("disabled")')
            except:
                has_next = False
            if has_next:
                self.driver.execute_script(
                    'document.querySelector(".ui_pagination>.next").click()')

        return [r.__dict__ for r in reviews]
