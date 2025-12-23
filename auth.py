from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.verify(password, password_hash)

def create_token(identity):
    # カスタマイズ可（有効期限等）
    return create_access_token(identity=identity, expires_delta=timedelta(hours=8))
