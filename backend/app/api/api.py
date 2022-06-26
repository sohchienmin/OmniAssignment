from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import requests
from pydantic import BaseModel, validator
from fastapi.responses import RedirectResponse, JSONResponse

from app.repositories.url_table_repository import (
    find_shortened_url,
    insert_url,
    find_original_url,
)
from app.helpers import build_shortened_url, generate_unique_key, get_fake_headers

app = FastAPI()

frontend_base_url = "http://localhost:3000"
backend_base_url = "http://localhost:8080"
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_base_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MAX_RETRIES = 10


class Data(BaseModel):
    url: str

    @validator("url")
    def url_must_not_have_whitespace(cls, value):
        if " " in value:
            raise ValueError("URL must not contain whitespace")
        return value

    @validator("url")
    def url_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("URL must not be empty")
        return value

    @validator("url")
    def url_does_not_exists(cls, value):
        try:
            response = requests.get(value, headers=get_fake_headers())
            if response.status_code == 200:
                return value
            else:
                raise Exception
        except Exception:
            raise ValueError("Invalid URL, please include the full URL with http/https")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


@app.post("/generate_url")
async def generate_url(data: Data):
    try:
        url = data.url
        shortened_url = find_shortened_url(url)

        if not shortened_url:
            unique_key = generate_unique_key()
            shortened_url = build_shortened_url(backend_base_url, unique_key)
            current_retry = 0

            # We should check if there is a collision, if there is, we need to regenerate the shortened url to be unique
            while find_original_url(shortened_url):
                if current_retry == MAX_RETRIES:
                    raise Exception("Reached limit of retries to generate unique key")
                unique_key = generate_unique_key()
                shortened_url = build_shortened_url(backend_base_url, unique_key)
                current_retry += 1

            insert_url(url, shortened_url)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"detail": [{"msg": str(e)}]}),
        )

    return {"url": shortened_url}


@app.get("/{unique_key}")
async def root(unique_key):
    shortened_url = build_shortened_url(backend_base_url, unique_key)
    original_url = find_original_url(shortened_url)

    if not original_url:
        raise HTTPException(status_code=404, detail="Invalid URL")

    return RedirectResponse(original_url)
