import bcrypt

async def hash_password(password: str) -> str:
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash.decode(encoding="utf-8", errors="strict")
