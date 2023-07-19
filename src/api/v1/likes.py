from fastapi import APIRouter, Depends, Request, HTTPException
from http import HTTPStatus
from api.v1.models.feedback import LikeReq, LikeDeleteReq
from api.v1.auth.auth_bearer import BaseJWTBearer
from services.like import LikeService, get_like_service
from services.auth import AuthApi

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/',
    description='Пост оценки (10 - лайк, 0 - дизлайк)',
    dependencies=[Depends(BaseJWTBearer())]
)
async def post_like(data: LikeReq, request: Request, like_service: LikeService = Depends(get_like_service)):
    if data.mark not in [0, 10]:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Mark value must be 0 or 10')
    current_user = request.token_payload
    res = await like_service.post_like(data, current_user['id'])
    return res


@router.put(
    '/',
    description='Изменение оценки: с 0 до 10 и наоборот',
    dependencies=[Depends(BaseJWTBearer())]
)
async def upd_like(data: LikeReq, request: Request, like_service: LikeService = Depends(get_like_service)):
    current_user = request.token_payload
    res = await like_service.update_like(data, current_user['id'])
    return res


@router.delete(
    '/',
    description='Удаление оценки',
    dependencies=[Depends(BaseJWTBearer())]
)
async def del_like(data: LikeDeleteReq, request: Request, like_service: LikeService = Depends(get_like_service)):
    current_user = request.token_payload
    res = await like_service.delete_like(data, current_user['id'])
    return res


@router.get(
    '/likes_avg/{film_id}',
    description='Вывод рейтинга фильма как среднего арифметического от лайков (10) и дизлайков (0)')
async def get_avg_like(film_id: str, like_service: LikeService = Depends(get_like_service)):
    res = await like_service.get_likes_avg(film_id)
    return res


@router.get(
    '/likes_count/{film_id}',
    description='Вывод количества лайков (оценок 10)',)
async def get_count_like(film_id: str, like_service: LikeService = Depends(get_like_service)):
    res = await like_service.count_likes(film_id)
    return res


@router.get(
    '/dislikes_count/{film_id}',
    description='Вывод количества дизлайков (оценок 0)',)
async def get_count_dislike(film_id: str, like_service: LikeService = Depends(get_like_service)):
    res = await like_service.count_dislikes(film_id)
    return res
