import bcrypt

async def check_password(password: str, hashed_password: str) -> bool:
    bytes_password = password.encode('utf-8')
    bytes_hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(bytes_password, bytes_hashed_password)