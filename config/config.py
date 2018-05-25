URL_PATTERN = 'http(s)?:\/\/.?(www\.)?tripadvisor\.(com|es)\/Restaurant_Review.*'
DEFAULT_LANGUAGE = "en"
SECONDS_BETWEEN_REQUEST = 1.5
I18N = {
    'en': {
        'more_btn': 'More',
        'date_format': '%B %d, %Y',
        'in': 'in'
    },
    'es': {
        'more_btn': 'Más',
        'date_format': '%d %B %Y',
        'in': 'en'
    }
}
RATING = {
    'bubble_50': 5,
    'bubble_45': 4.5,
    'bubble_40': 4,
    'bubble_35': 3.5,
    'bubble_30': 3,
    'bubble_25': 2.5,
    'bubble_20': 2,
    'bubble_15': 1.5,
    'bubble_10': 1
}

PRICE = {
    'en': {
        '$': 1,
        '$-$$': 1.5,
        '$$': 2,
        '$$-$$$': 2.5,
        '$$$': 3,
        '$$$-$$$$': 3.5,
        '$$$$': 4
    },
    'es': {
        '€': 1,
        '€-€€': 1.5,
        '€€': 2,
        '€€-€€€': 2.5,
        '€€€': 3,
        '€€€-€€€€': 3.5,
        '€€€€': 4
    }
}

TIME_BETWEEEN_UPDATE = 60*60*24*30
