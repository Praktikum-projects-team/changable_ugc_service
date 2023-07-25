from http import HTTPStatus

import pytest

from tests.functional.testdata.reviews import get_reviews_post_data, get_reviews_evaluate_data
from tests.functional.utils.routes import REVIEWS_URL, REVIEWS_LIKE_URL, REVIEWS_DISLIKE_URL
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE

pytestmark = pytest.mark.asyncio


class TestReview:
    async def test_review_adding(self, make_post_request, make_delete_request, user_access_token):
        review_data = await get_reviews_post_data()
        resp = await make_post_request(REVIEWS_URL, data=review_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Review successfully posted', 'Wrong message'

    @pytest.mark.parametrize('sort, page_size, page_number, len_response', [
        ('-publication_date', DEFAULT_PAGE_SIZE, 1, DEFAULT_PAGE_SIZE),
        ('likes', DEFAULT_PAGE_SIZE + 1, 1, DEFAULT_PAGE_SIZE + 1),
        ('dislikes', 1, 1, 1)])
    async def test_reviews_get_all(self, make_post_request, make_get_request,
                                   make_delete_request, user_access_token,
                                   sort, page_size, page_number, len_response):
        review_data = await get_reviews_post_data(n=DEFAULT_PAGE_SIZE)
        for review in review_data:
            await make_post_request(REVIEWS_URL, data=review, token=user_access_token)

        resp = await make_get_request(
            f"{REVIEWS_URL}?sort={sort}&page_size={page_size}&page_number={page_number}")

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert len(resp.body) == len_response, 'Wrong message'

    @pytest.mark.parametrize('field', ['incorrect_field', 1, 'text'])
    async def test_reviews_get_all_incorrect_sort(self, make_post_request, make_get_request,
                                                  make_delete_request, user_access_token, field):
        review_data = await get_reviews_post_data(n=DEFAULT_PAGE_SIZE)
        for review in review_data:
            await make_post_request(REVIEWS_URL, data=review, token=user_access_token)

        resp = await make_get_request(f"{REVIEWS_URL}?sort={field}")

        assert resp.status == HTTPStatus.BAD_REQUEST, 'Wrong status code'
        assert resp.body['detail'] == f'{field} is not suitable for sorting', 'Wrong message'

    async def test_review_like(self, make_post_request, make_delete_request, user_access_token):
        review_data = await get_reviews_post_data()
        post_resp = await make_post_request(REVIEWS_URL, data=review_data[0], token=user_access_token)
        review_like_data = await get_reviews_evaluate_data(review_id=post_resp.body['review_id'])
        resp = await make_post_request(REVIEWS_LIKE_URL, data=review_like_data[0], token=user_access_token)

        await make_delete_request(REVIEWS_LIKE_URL, data=review_like_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Review successfully rated', 'Wrong message'

    async def test_review_re_evaluate(self, make_post_request, make_delete_request, user_access_token):
        review_data = await get_reviews_post_data()
        post_resp = await make_post_request(REVIEWS_URL, data=review_data[0], token=user_access_token)
        review_like_data = await get_reviews_evaluate_data(review_id=post_resp.body['review_id'])
        await make_post_request(REVIEWS_LIKE_URL, data=review_like_data[0], token=user_access_token)
        resp = await make_post_request(REVIEWS_DISLIKE_URL, data=review_like_data[0],
                                       token=user_access_token)

        await make_delete_request(REVIEWS_LIKE_URL, data=review_like_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'You have already rated this review', 'Wrong message'

    async def test_review_dislike(self, make_post_request, make_delete_request, user_access_token):
        review_data = await get_reviews_post_data()
        post_resp = await make_post_request(REVIEWS_URL, data=review_data[0], token=user_access_token)
        review_like_data = await get_reviews_evaluate_data(review_id=post_resp.body['review_id'])
        resp = await make_post_request(REVIEWS_DISLIKE_URL, data=review_like_data[0],
                                       token=user_access_token)

        await make_delete_request(REVIEWS_DISLIKE_URL, data=review_like_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Review successfully rated', 'Wrong message'

    async def test_incorrect_review_evaluate(self, make_post_request, make_delete_request,
                                             user_access_token):
        review_like_data = await get_reviews_evaluate_data()
        resp = await make_post_request(REVIEWS_DISLIKE_URL, data=review_like_data[0],
                                       token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Review not found', 'Wrong message'
