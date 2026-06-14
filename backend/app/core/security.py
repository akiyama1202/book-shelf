from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# パスワードのハッシュ化・検証に使う設定。argon2というハッシュアルゴリズムを使用する。
_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    # 平文パスワードをハッシュ化する（DBには平文を保存せず、この戻り値を保存する）。
    return _pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # ログイン時、入力された平文パスワードがDBに保存されたハッシュ値と一致するか検証する。
    return _pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    # ログイン成功時に発行するJWT（アクセストークン）を作成する。
    # subject: トークンの持ち主を識別する値（通常はユーザーIDなど）
    # expires_delta: 有効期限を個別指定したい場合に渡す（省略時は設定値のデフォルトを使う）
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    # "sub"(subject)と"exp"(有効期限)を含むペイロードを、秘密鍵で署名してトークン文字列にする。
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    # リクエストで送られてきたJWTを検証・復号する。
    # 署名が不正・期限切れなどの場合はJWTErrorが発生するので、ValueErrorに変換して伝える。
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError as exc:
        raise ValueError("Invalid token") from exc
