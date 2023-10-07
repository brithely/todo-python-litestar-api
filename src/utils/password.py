import base64
import hashlib
import secrets

ALGORITHM = "pbkdf2_sha256"


def hash_password(password: str, salt=None, iterations=100000) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    assert salt and isinstance(salt, str) and "$" not in salt
    assert isinstance(password, str)
    pw_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations
    )
    b64_hash = base64.b64encode(pw_hash).decode("ascii").strip()
    return f"{ALGORITHM}${iterations}${salt}${b64_hash}"


def get_password_salf(hashed_password: str) -> str:
    algorithm, iterations, salt, pw_hash = hashed_password.split("$")
    assert algorithm == ALGORITHM
    return salt
