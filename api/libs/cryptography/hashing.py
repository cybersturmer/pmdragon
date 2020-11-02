import hashlib

from django.conf import settings


def get_hash(*args) -> str:
    """
    Convert to String all given args
    Adding SECRET_KEY and hashing it with sha3_256
    @param args: Any argument convertible to String
    @return: String with HEX digest
    """
    hashing_list = []
    for arg in args:
        hashing_list.append(str(arg))
    hashing_list.append(settings.SECRET_KEY)
    hashing_string = ''.join(hashing_list)
    return hashlib.sha3_256(hashing_string.encode('utf-8')).hexdigest()
