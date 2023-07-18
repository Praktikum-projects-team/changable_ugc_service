from fastapi import APIRouter, Depends, Request
from src.api.v1.models.feedback import BookmarkReq
from src.api.v1.auth.auth_bearer import BaseJWTBearer
from src.services.bookmark import BookmarkService, get_bookmark_service
from src.services.auth import AuthApi

router = APIRouter()
auth_api = AuthApi()


@router.get(
    '/',
    description='Просмотр закладок текущего пользователя',
    dependencies=[Depends(BaseJWTBearer())]
)
async def get_bookmarks(request: Request, bookmark_service: BookmarkService = Depends(get_bookmark_service)):
    current_user = request.token_payload
    bookmarks = await bookmark_service.get_all(current_user['id'])

    return bookmarks


@router.post(
    '/',
    description='Добавление фильма в закладки',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_bookmark(data: BookmarkReq, request: Request, bookmark_service: BookmarkService = Depends(get_bookmark_service)):
    current_user = request.token_payload
    res = await bookmark_service.post_bookmark(data, current_user['id'])
    return res


@router.delete(
    '/',
    description='Удаление фильма из закладок',
    dependencies=[Depends(BaseJWTBearer())]
)
async def delete_bookmark(data: BookmarkReq, request: Request, bookmark_service: BookmarkService = Depends(get_bookmark_service)):
    current_user = request.token_payload
    res = await bookmark_service.delete_bookmark(data, current_user['id'])
    return res


