from tests.functional.settings import test_settings

BASE_URL = '/api/v1'


LIKES_URL = f'{BASE_URL}/likes'
LIKES_URL_AVG = f'{BASE_URL}/likes/likes_avg'
LIKES_URL_COUNT = f'{BASE_URL}/likes/likes_count'
DISLIKES_URL_COUNT = f'{BASE_URL}/likes/dislikes_count'
BOOKMARKS_URL = f'{BASE_URL}/bookmarks'
REVIEWS_URL = f'{BASE_URL}/reviews'


AUTH_URL_SIGN_UP = f'{test_settings.auth_host}/api/v1/auth/sign_up'
AUTH_URL_LOGIN = f'{test_settings.auth_host}/api/v1/auth/login'