from pymongo import MongoClient


def create_session():
    client = MongoClient(port=27017)
    db = client.tripadvisor
    return db


def restaurant_already_exists(db, restaurant_id):
    return db.restaurant.find({'_id': restaurant_id}).count() > 0


def review_already_exists(db, review_id):
    return db.review.find({'_id': review_id}).count() > 0


def insert_restaurant_data(db, restaurant):
    if restaurant_already_exists(db, restaurant['_id']):
        db.restaurant.replace_one({'_id': restaurant['_id']}, restaurant)
    else:
        db.restaurant.insert(restaurant)


def insert_reviews_data(db, reviews):
    for review in reviews:
        if review_already_exists(db, review['_id']):
            db.review.replace_one({'_id': review['_id']}, review)
        else:
            db.review.insert(review)

