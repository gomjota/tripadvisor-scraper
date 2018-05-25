import json
import time


class Restaurant:
    def __init__(self, _id, name, rating, ranking_position, price, tags, address, phone, cuisines, ratings):
        self._id = _id
        self.name = name
        self.rating = rating
        self.ranking_position = ranking_position
        self.price = price
        self.tags = tags
        self.address = address
        self.phone = phone
        self.cuisines = cuisines
        self.ratings = ratings
        self.updated_at = int(time.time())

    def obj_dict(self, obj):
        return obj.__dict__

    def to_dict(self):
        return {
            '_id': self._id,
            'name': self.name,
            'rating': self.rating,
            'ranking_position': self.ranking_position,
            'price': self.price,
            'tags': self.tags,
            'address': json.dumps(self.address.__dict__),
            'phone': self.phone,
            'cuisines': self.cuisines,
            'ratings': json.dumps(self.ratings, default=self.obj_dict),
            'updated_at': self.updated_at
        }
