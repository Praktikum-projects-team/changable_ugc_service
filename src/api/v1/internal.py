from fastapi import APIRouter, Depends
from services.bookmark import BookmarkService, get_bookmark_service
from services.auth import AuthApi

router = APIRouter()
auth_api = AuthApi()


@router.get(
    '/bookmarks/{user_id}',
    description='Просмотр закладок пользователя по его uuid'
)
async def get_user_bookmarks(
        user_id: str,
        bookmark_service: BookmarkService = Depends(get_bookmark_service)):
    bookmarks = await bookmark_service.get_all(user_id)

    return bookmarks
