import hashlib
import pickle

# Helper to hash bytes
def hash_it(data: bytes) -> str:
    js = pickle.dumps(data, protocol=4)
    return hashlib.sha256(js).hexdigest()[:16]  # short for readability
