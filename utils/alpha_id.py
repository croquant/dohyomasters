import os
import time

from utils import base26


def alpha_id():
    timestamp = int(time.time() * 1000)
    timestamp_bytes = timestamp.to_bytes(6, byteorder="little")
    random_bytes = os.urandom(3)
    combined_bytes = random_bytes + timestamp_bytes
    base26_string = base26.encode(combined_bytes)
    return base26_string[::-1]
