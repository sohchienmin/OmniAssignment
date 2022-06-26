import uuid


def build_shortened_url(base_url: str, unique_key: str):
    return base_url + "/" + unique_key


def generate_unique_key():
    return uuid.uuid4().hex[:10]


def get_fake_headers():
    return {"User-Agent": "Mozilla 5.0"}
