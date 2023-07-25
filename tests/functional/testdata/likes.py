import uuid

film_id = str(uuid.uuid4())


async def get_likes_post_data(n: int = 1, mark: int = 10) -> list[dict]:
    return [{
        'film_id': film_id,
        'mark': mark
    } for _ in range(n)]


async def get_likes_update_data(n: int = 1) -> list[dict]:
    return [{
        'film_id': film_id,
        'mark': 0
    } for _ in range(n)]


async def get_likes_delete_data(n: int = 1) -> list[dict]:
    return [{
        'film_id': film_id
    } for _ in range(n)]
