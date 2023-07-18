from src.core.base_model import OrjsonBaseModel
from uuid import UUID
from datetime import datetime


class LikeReq(OrjsonBaseModel):
    film_id: str
    mark: int


class LikeDeleteReq(OrjsonBaseModel):
    film_id: str


class BookmarkReq(OrjsonBaseModel):
    film_id: str


class BookmarkResp(OrjsonBaseModel):
    film_id: UUID


class ReviewReq(OrjsonBaseModel):
    film_id: str
    text: str
    publication_date: datetime = datetime.now()


class ReviewLike(OrjsonBaseModel):
    review_id: str
