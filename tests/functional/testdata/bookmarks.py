import uuid


async def get_bookmarks_post_data(n: int = 1) -> list[dict]:
    return [{
        'film_id': str(uuid.uuid4())
    } for _ in range(n)]
