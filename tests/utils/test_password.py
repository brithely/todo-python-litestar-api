from src.utils.password import ALGORITHM, hash_password


def test_hash_password_would_return_hashed_password():
    password = "test"
    hashed_password = hash_password(password)
    assert hashed_password != password
    assert hashed_password.startswith(f"{ALGORITHM}$")


def test_hash_password_would_return_same_hashed_password_given_same_password():
    password = "test"
    salt = "salt"
    hashed_password = hash_password(password, salt)
    assert hashed_password == hash_password(password, salt)


def test_hash_password_would_return_different_hashed_password_given_different_password():
    password1 = "test1"
    password2 = "test2"
    hashed_password1 = hash_password(password1)
    hashed_password2 = hash_password(password2)
    assert hashed_password1 != hashed_password2


def test_hash_password_would_return_different_hashed_password_given_different_salt():
    password = "test"
    hashed_password1 = hash_password(password, salt="salt1")
    hashed_password2 = hash_password(password, salt="salt2")
    assert hashed_password1 != hashed_password2
