import datetime
from pprint import pprint as pp

from pymongo import MongoClient


def get_database() -> MongoClient:
    client = MongoClient(host="127.0.0.1", port=27017)
    return client


if __name__ == "__main__":
    print("start")
    client = get_database()
    print(1)
    db = client['feedback']
    print(db)
    collection = db['likes']
    # print(db.list_collection_names())
    post = {"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860b",
            "film_id": "d4f281ad-fb96-410b-bb76-d4fe508b2815",
            "mark": 0}
    # posts = db.posts
    post_id = collection.insert_one(post).inserted_id
    # print(post_id)
    # print(db.posts.find_one())
    post2 = {"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860h",
            "film_id": "d4f281ad-fb96-410b-bb76-d4fe508b2814",
            "mark": 0}
    for post1 in collection.find({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860b"}).sort("film_id"):
        print(post1)
    print(db.likes.count_documents({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860b"}))
    print(db.likes.find_one_and_update({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860u"}, {'$set': {'mark': 8}}))
    for post1 in collection.find({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860b"}).sort("film_id"):
        print(post1['mark'])
    print(db.likes.count_documents({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860b"}))
    print(db.likes.delete_one({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860c"}).deleted_count)
    # print(db.likes.count_documents({"user_id": "d4368a1e-31ef-48b5-beda-7128bb03860b"}))
