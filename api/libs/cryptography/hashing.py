import hashlib

from django.conf import settings


def get_hash(raw_string: str) -> str:
    raw_string += settings.SECRET_KEY
    return hashlib.sha3_256(raw_string.encode('utf-8')).hexdigest()
