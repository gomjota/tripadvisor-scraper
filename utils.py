import locale
import re
import logging

from config.config import URL_PATTERN


def is_valid_url(url):
    return re.compile(URL_PATTERN).match(url)


def set_locale(url=''):
    if 'tripadvisor.es' in url:
        locale.setlocale(locale.LC_TIME, 'es_ES')
    elif 'tripadvisor.com' in url:
        locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    else:
        logging.warn('Tripadvisor domain location not supported. Defaulting to English (.com)')


def get_language_by_url(url):
    if 'tripadvisor.es' in url:
        return 'es'
    elif 'tripadvisor.com' in url:
        return 'en'
    return None


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_id_by_url(url):
    if not is_valid_url(url): return None
    match = re.compile('.*Restaurant_Review-g\d+-(d\d+).*').match(url)
    if match is None: return None
    return match.group(1)
