from functools import lru_cache
from motor.motor_asyncio import AsyncIOMotorDatabase
from db.mongo_db import init_db
from bson.objectid import ObjectId
from api.v1.utils import Page


class ReviewService:
    def __init__(self, mongo: AsyncIOMotorDatabase):
        self.mongo_db = mongo
        self.collection = self.mongo_db.reviews
        self.ratings_collection = self.mongo_db.reviews_ratings
        self.likes_collection = self.mongo_db.likes

    async def post_review(self, data, user_data):
        if await self.likes_collection.find_one({"user_id": user_data['id'], "film_id": data.film_id}) is not None:
            users_likes = await self.likes_collection.find_one({"user_id": user_data['id'], "film_id": data.film_id})
            mark = users_likes['mark']
        else:
            mark = 0
        res = await self.collection.insert_one(
            {"user_id": user_data['id'], "user_name": user_data['name'],
             "film_id": data.film_id, "text": data.text,
             "publication_date": data.publication_date,
             "likes": 0, "dislikes": 0, "mark": mark})
        review_id = res.inserted_id

        return {'msg': 'Review successfully posted', 'review_id': str(review_id)}

    async def get_all(self, sorting, page: Page):
        reviews_list = []
        async for review in self.collection.find(sort=sorting).skip(page.page_from):
            reviews_list.append({'publication_date': review['publication_date'],
                                 'film_id': review['film_id'], 'user_id': review['user_id'],
                                 'user_name': review['user_name'], 'likes': review['likes'],
                                 'dislikes': review['dislikes'], 'mark': review['mark'],
                                 'text': review['text']})

        return reviews_list

    async def evaluate_review(self, data, user_id, like: bool):
        if await self.ratings_collection.find_one({"user_id": user_id, "review_id": data.review_id}) is None:
            review_info = await self.collection.find_one({"_id": ObjectId(data.review_id)})
            if like:
                likes_count = 0
                if review_info:
                    likes_count = review_info['likes']
                res = await self.collection.find_one_and_update({"_id": ObjectId(data.review_id)},
                                                                {'$set': {'likes': likes_count + 1}})
            else:
                dislikes_count = 0
                if review_info:
                    dislikes_count = await review_info['dislikes']
                res = await self.collection.find_one_and_update({"_id": ObjectId(data.review_id)},
                                                                {'$set': {'dislikes': dislikes_count + 1}})
            await self.ratings_collection.insert_one({"user_id": user_id, "review_id": data.review_id})
        else:
            return {'msg': 'You have already rated this review'}
        if res:
            return {'msg': 'Review successfully rated'}

        return {'msg': 'Review not found'}


@lru_cache()
def get_review_service() -> ReviewService:
    mongo = init_db()
    return ReviewService(mongo)
