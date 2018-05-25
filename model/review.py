import time


class Review:
    def __init__(self, _id, restaurant_id, date, title, user, text, rating, via_mobile, language):
        self._id = _id
        self.restaurant_id = restaurant_id
        self.date = date
        self.title = title
        self.user = user
        self.text = text
        self.rating = rating
        self.via_mobile = via_mobile
        self.language = language
