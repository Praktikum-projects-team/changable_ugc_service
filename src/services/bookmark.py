from functools import lru_cache
from db.mongo_db import init_db
from api.v1.utils import Page


class BookmarkService:
    def __init__(self, mongo):
        self.mongo_db = mongo
        self.collection = self.mongo_db.bookmarks

    async def post_bookmark(self, data, user_id):
        if self.collection.find_one({"user_id": user_id, "film_id": data.film_id}) is None:
            self.collection.insert_one({"user_id": user_id, "film_id": data.film_id})
            return {'msg': f'Added {data.film_id} in bookmarks'}

        return {'msg': f'Movie {data.film_id} is already in bookmarks'}

    async def get_all(self, user_id, page: Page):
        bookmarks_list = []
        for bookmark in self.collection.find({"user_id": user_id}).skip(page.page_from):
            bookmarks_list.append(bookmark['film_id'])

        return bookmarks_list

    async def delete_bookmark(self, data, user_id):
        res = self.collection.delete_one({"user_id": user_id, "film_id": data.film_id})
        if res.deleted_count > 0:
            return {'msg': f'Deleted {data.film_id} from bookmarks'}

        return {'msg': 'Bookmark not found'}


@lru_cache()
def get_bookmark_service() -> BookmarkService:
    mongo = init_db()
    return BookmarkService(mongo)
