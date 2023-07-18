from fastapi import APIRouter, Depends, Request
from src.api.v1.models.feedback import ReviewReq, ReviewLike
from src.api.v1.auth.auth_bearer import BaseJWTBearer
from src.services.review import ReviewService, get_review_service
from src.services.auth import AuthApi
from src.api.v1.utils import SortReview
from src.api.v1.utils import Page

router = APIRouter()
auth_api = AuthApi()


@router.post(
    '/',
    description='Добавление рецензии',
    dependencies=[Depends(BaseJWTBearer())]
)
async def add_review(data: ReviewReq, request: Request,
                     review_service: ReviewService = Depends(get_review_service)):
    current_user = request.token_payload
    res = await review_service.post_review(data, current_user)
    return res


@router.get(
    '/',
    description='Просмотр списка рецензий'
)
async def get_reviews(sort: SortReview = Depends(), page: Page = Depends(),
                      review_service: ReviewService = Depends(get_review_service)):
    reviews = await review_service.get_all(sort.sort, page)

    return reviews


@router.post(
    '/like',
    description='Лайк рецензии',
    dependencies=[Depends(BaseJWTBearer())]
)
async def like_review(data: ReviewLike, request: Request,
                      review_service: ReviewService = Depends(get_review_service)):
    current_user = request.token_payload
    res = await review_service.evaluate_review(data, current_user['id'], True)
    return res


@router.post(
    '/dislike',
    description='Дизлайк рецензии',
    dependencies=[Depends(BaseJWTBearer())]
)
async def dislike_review(data: ReviewLike, request: Request,
                         review_service: ReviewService = Depends(get_review_service)):
    current_user = request.token_payload
    res = await review_service.evaluate_review(data, current_user['id'], False)
    return res
