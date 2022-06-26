from sqlalchemy import text

from app.repositories.database import open_connection


def insert_url(original_url: str, shortened_url: str):
    with open_connection() as connection:
        connection.execute(
            INSERT_QUERY, original_url=original_url, shortened_url=shortened_url
        )


def find_shortened_url(original_url: str) -> str:
    with open_connection() as connection:
        result = connection.execute(
            FIND_SHORTENED_URL_QUERY, original_url=original_url
        ).fetchone()

    return result["shortened_url"] if result else ""


def find_original_url(shortened_url: str) -> str:
    with open_connection() as connection:
        result = connection.execute(
            FIND_ORIGINAL_URL_QUERY, shortened_url=shortened_url
        ).fetchone()

    return result["original_url"] if result else ""


INSERT_QUERY = text(
    "INSERT INTO url_table (original_url, shortened_url) VALUES (:original_url, :shortened_url)"
)
FIND_SHORTENED_URL_QUERY = text(
    "SELECT shortened_url FROM url_table WHERE original_url = :original_url"
)
FIND_ORIGINAL_URL_QUERY = text(
    "SELECT original_url FROM url_table WHERE shortened_url = :shortened_url"
)
