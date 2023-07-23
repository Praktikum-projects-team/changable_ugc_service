import uuid


async def get_reviews_post_data(n: int = 1) -> list[dict]:
    return [{
        'film_id': str(uuid.uuid4()),
        'text': 'This film is so good'
    } for _ in range(n)]


async def get_reviews_evaluate_data(n: int = 1, review_id: str = '123456789') -> list[dict]:
    return [{
        'review_id': review_id
    } for _ in range(n)]
