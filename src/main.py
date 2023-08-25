import logging
from http import HTTPStatus

import sentry_sdk
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import ORJSONResponse
from httpx import RequestError

from api.v1 import likes, bookmarks, reviews, internal
from core.logger import LOGGING
from core.config import (app_config, sentry_config)

from dotenv import load_dotenv

load_dotenv()

sentry_sdk.init(
    dsn=sentry_config.dns,
    traces_sample_rate=0.4,
)

app = FastAPI(
    title=app_config.project_name,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
)

app.include_router(likes.router, prefix='/api/v1/likes', tags=['likes'])
app.include_router(bookmarks.router, prefix='/api/v1/bookmarks', tags=['bookmarks'])
app.include_router(reviews.router, prefix='/api/v1/reviews', tags=['reviews'])
app.include_router(internal.router, prefix='/internal', tags=['internal'])


@app.exception_handler(RequestError)
async def bad_storage_request_exception_handler(request, exc):
    http_exc = HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=exc.error)
    return await http_exception_handler(request, http_exc)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=app_config.host,
        port=app_config.port,
        log_config=LOGGING,
        log_level=logging.DEBUG if app_config.is_debug else logging.INFO,
    )
