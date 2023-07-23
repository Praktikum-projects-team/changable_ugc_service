from http import HTTPStatus

import pytest

from tests.functional.testdata.bookmarks import get_bookmarks_post_data
from tests.functional.utils.routes import BOOKMARKS_URL
from tests.functional.utils.constants import DEFAULT_PAGE_SIZE

pytestmark = pytest.mark.asyncio


class TestBookmark:
    async def test_bookmark_adding(self, make_post_request, make_delete_request, user_access_token):
        bookmark_data = await get_bookmarks_post_data()
        resp = await make_post_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)

        del_resp = await make_delete_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert resp.body['msg'] == f"Added {bookmark_data[0]['film_id']} in bookmarks", 'Wrong message'

    @pytest.mark.parametrize('page_size', [1, 15, 20, 21, '10'])
    async def test_bookmark_getting(self, make_post_request, make_get_request, make_delete_request, user_access_token, page_size):
        bookmark_data = await get_bookmarks_post_data(n=DEFAULT_PAGE_SIZE)
        await make_post_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
        resp = make_get_request(BOOKMARKS_URL, {'page_size': page_size}, token=user_access_token)

        await make_delete_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)

        assert resp.status == HTTPStatus.OK, 'Wrong status code'
        assert len(resp.body) == int(page_size), 'Wrong page size in response'
