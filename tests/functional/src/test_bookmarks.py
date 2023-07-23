# from http import HTTPStatus
#
# import pytest
#
# from tests.functional.testdata.bookmarks import get_bookmarks_post_data
# from tests.functional.utils.routes import BOOKMARKS_URL
# from tests.functional.utils.constants import DEFAULT_PAGE_SIZE
#
# pytestmark = pytest.mark.asyncio
#
#
# class TestBookmark:
#     async def test_bookmark_adding(self, make_post_request, make_delete_request, user_access_token):
#         bookmark_data = await get_bookmarks_post_data()
#         resp = await make_post_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         await make_delete_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         assert resp.status == HTTPStatus.OK, 'Wrong status code'
#         assert resp.body['msg'] == f"Added {bookmark_data[0]['film_id']} in bookmarks", 'Wrong message'
#
#     async def test_adding_existing_bookmark(self, make_post_request, make_delete_request, user_access_token):
#         bookmark_data = await get_bookmarks_post_data()
#         await make_post_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#         resp = await make_post_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         await make_delete_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         assert resp.status == HTTPStatus.OK, 'Wrong status code'
#         assert resp.body['msg'] == f"Movie {bookmark_data[0]['film_id']} is already in bookmarks", 'Wrong message'
#
#     async def test_bookmark_getting(self, make_post_request, make_get_request_with_token, make_delete_request,
#                                     user_access_token):
#         bookmark_data = await get_bookmarks_post_data(n=DEFAULT_PAGE_SIZE)
#         for bookmark in bookmark_data:
#             await make_post_request(BOOKMARKS_URL, data=bookmark, token=user_access_token)
#         resp = await make_get_request_with_token(path=f"{BOOKMARKS_URL}?page_size={DEFAULT_PAGE_SIZE - 1}", token=user_access_token)
#         resp_page_numb = await make_get_request_with_token(path=f"{BOOKMARKS_URL}?page_size={DEFAULT_PAGE_SIZE - 1}?page_number={2}",
#                                                            token=user_access_token)
#
#         for bookmark in bookmark_data:
#             await make_delete_request(BOOKMARKS_URL, data=bookmark, token=user_access_token)
#
#         assert resp.status == HTTPStatus.OK, 'Wrong status code'
#         assert len(resp.body) == DEFAULT_PAGE_SIZE - 1, 'Wrong page size in response'
#         assert len(resp_page_numb.body) == 1, 'Wrong page size in response'
#
#     async def test_bookmark_deletion(self, make_post_request, make_delete_request, user_access_token):
#         bookmark_data = await get_bookmarks_post_data()
#         await make_post_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         resp = await make_delete_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         assert resp.status == HTTPStatus.OK, 'Wrong status code'
#         assert resp.body['msg'] == f"Deleted {bookmark_data[0]['film_id']} from bookmarks", 'Wrong message'
#
#     async def test_bookmark_deletion_incorrect_film(self, make_post_request, make_delete_request, user_access_token):
#         bookmark_data = await get_bookmarks_post_data()
#         resp = await make_delete_request(BOOKMARKS_URL, data=bookmark_data[0], token=user_access_token)
#
#         assert resp.status == HTTPStatus.OK, 'Wrong status code'
#         assert resp.body['msg'] == 'Bookmark not found', 'Wrong message'
