from pymongo import DESCENDING, ASCENDING
from http import HTTPStatus
from fastapi import HTTPException, Query
from core.config import app_config


class SortReview:
    SORTABLE_FIELDS = ('publication_date', 'likes', 'dislikes',)

    def __init__(self, sort: str = '-publication_date'):
        sort_type = DESCENDING if sort[0] == '-' else ASCENDING
        sort_field = sort[1:] if sort[0] == '-' else sort
        if sort_field not in self.SORTABLE_FIELDS:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=f'{sort_field} is not suitable for sorting')
        self.sort = [(sort_field, sort_type)]


class Page:
    def __init__(
            self,
            page_size: int = Query(app_config.default_page_size, ge=1),
            page_number: int = Query(1, ge=1)
    ) -> None:
        self.page_size = page_size
        self.page_number = page_number

    @property
    def page_from(self):
        return self.page_size * (self.page_number - 1)
