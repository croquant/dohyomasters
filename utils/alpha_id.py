import os
import time
from base64 import b32encode


def alpha_id():
    timestamp = int(time.time() * 1000)
    timestamp_bytes = timestamp.to_bytes(6, byteorder="big")
    random_bytes = os.urandom(4)
    combined_bytes = timestamp_bytes + random_bytes
    base32_string = b32encode(combined_bytes).decode("utf-8")
    return base32_string.lower()
