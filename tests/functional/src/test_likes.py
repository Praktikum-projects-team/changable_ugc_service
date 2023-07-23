from http import HTTPStatus

import pytest

from tests.functional.testdata.likes import get_likes_post_data, get_likes_update_data, get_likes_delete_data
from tests.functional.utils.routes import LIKES_URL, LIKES_URL_AVG, LIKES_URL_COUNT, DISLIKES_URL_COUNT

pytestmark = pytest.mark.asyncio


class TestLikes:
    async def test_like_adding(self, make_post_request, user_access_token):
        like_data = await get_likes_post_data()
        resp = await make_post_request(LIKES_URL, data=like_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == f"Posted film score: {like_data[0]['mark']}", 'Wrong message'

    async def test_like_updating(self, make_put_request, user_access_token):
        like_data = await get_likes_update_data()
        resp = await make_put_request(LIKES_URL, data=like_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == f"Updated film score to {like_data[0]['mark']}", 'Wrong message'

    async def test_like_deletion(self, make_delete_request, user_access_token):
        like_data = await get_likes_delete_data()
        resp = await make_delete_request(LIKES_URL, data=like_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == 'Deleted like', 'Wrong message'

    async def test_likes_avg(self, make_get_request, make_post_request, make_delete_request, user_access_token):
        like_data = await get_likes_post_data()
        post_resp = await make_post_request(LIKES_URL, data=like_data[0], token=user_access_token)
        resp = await make_get_request(f"{LIKES_URL_AVG}/{like_data[0]['film_id']}")

        like_delete_data = await get_likes_delete_data()
        del_resp = await make_delete_request(LIKES_URL, data=like_delete_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['avg'] == 10, 'Wrong message'

    async def test_likes_count(self, make_get_request, make_post_request, user_access_token):
        like_data = await get_likes_post_data()
        post_resp = await make_post_request(LIKES_URL, data=like_data[0], token=user_access_token)
        resp = await make_get_request(f"{LIKES_URL_COUNT}/{like_data[0]['film_id']}")

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['likes_numb'] == 1, 'Wrong message'

    async def test_dislikes_count(self, make_get_request, make_post_request, user_access_token):
        like_data = await get_likes_post_data(mark=0)
        post_resp = await make_post_request(LIKES_URL, data=like_data[0], token=user_access_token)
        resp = await make_get_request(f"{DISLIKES_URL_COUNT}/{like_data[0]['film_id']}")

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['dislikes_numb'] == 1, 'Wrong message'
