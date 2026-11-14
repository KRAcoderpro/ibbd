from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from . import errors


class JWTEncryption:
    def __init__(
            self,
            secret_key: str,
            algorithm: str,
            expire_time: float,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_time = expire_time

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self._expire_time)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)
        return encoded_jwt

    def verify_jwt_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])

            expire_time: float = payload.get("exp")

            current_time = datetime.now(timezone.utc).timestamp()

            if current_time > expire_time:
                raise errors.TokenExpiredError()
        except JWTError:
            raise errors.TokenVerificationError()

        return payload
