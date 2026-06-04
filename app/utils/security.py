from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash = PasswordHash([Argon2Hasher()])


def get_password_hash(password: str, salt: bytes | None) -> str:
    return password_hash.hash(password, salt=salt)


def verify_password(plain_password: str, hashed_password: str) -> tuple[bool, str | None]:
    is_valid, updated_hash = password_hash.verify_and_update(plain_password, hashed_password)
    return is_valid, updated_hash
