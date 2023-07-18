from functools import lru_cache

from fastapi import Depends
from src.db.mongo_db import init_db


class LikeService:
    def __init__(self, mongo):
        self.mongo_db = mongo
        self.collection = self.mongo_db.likes

    async def post_like(self, data, user_id):
        if self.collection.find_one({"user_id": user_id, "film_id": data.film_id}) is None:
            self.collection.insert_one({"user_id": user_id, "film_id": data.film_id, "mark": data.mark})
            return {'msg': f'Posted film score: {data.mark}'}

        return {'msg': f'Like already exists'}

    async def update_like(self, data, user_id):
        res = self.collection.find_one_and_update({"user_id": user_id, "film_id": data.film_id},
                                                  {'$set': {'mark': data.mark}})
        if res:
            return {'msg': f'Updated film score to {data.mark}'}

        return {'msg': f'Film score not found'}

    async def delete_like(self, data, user_id):
        res = self.collection.delete_one({"user_id": user_id, "film_id": data.film_id})
        if res.deleted_count > 0:
            return {'msg': 'Deleted like'}

        return {'msg': 'Like not found'}

    async def get_likes_avg(self, film_id):
        sum, cnt = 0, 0
        avg = 0
        for doc in self.collection.find({"film_id": film_id}):
            cnt += 1
            sum += doc['mark']
        if cnt > 0:
            avg = round(sum / cnt, 2)

        return {'avg': avg}

    async def count_likes(self, film_id):
        count = self.collection.count_documents({"film_id": film_id, "mark": 10})
        return {'likes_numb': count}

    async def count_dislikes(self, film_id):
        count = self.collection.count_documents({"film_id": film_id, "mark": 0})
        return {'dislikes_numb': count}


@lru_cache()
def get_like_service() -> LikeService:
    mongo = init_db()
    return LikeService(mongo)
