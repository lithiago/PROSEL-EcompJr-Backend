from datetime import datetime, timedelta
from typing import Any

import jwt

from src.errors.errors import RegisterError
from src.core.config import JWT_SECRET, JWT_TEMPO_DE_EXPIRACAO, JWT_ALGORITMO
from pwdlib import PasswordHash


PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 128


senha_hash = PasswordHash.recommended()


def validar_senha(password: str) -> None:
    if len(password) < PASSWORD_MIN_LENGTH:
        raise RegisterError(
            "INVALID_PASSWORD",
            "A senha deve ter no minimo 8 caracteres.",
            {"field": "password", "rule": "min_length", "min_length": PASSWORD_MIN_LENGTH},
        )
    if len(password) > PASSWORD_MAX_LENGTH:
        raise RegisterError(
            "INVALID_PASSWORD",
            "A senha deve ter no maximo 128 caracteres.",
            {"field": "password", "rule": "max_length", "max_length": PASSWORD_MAX_LENGTH},
        )


def get_senha_hash(senha: str):
    return senha_hash.hash(senha)

def comparar_senhas(password: str, password_hash: str):
    return senha_hash.verify(password, password_hash)

def create_access_token(subject: str | Any, role: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(hours=JWT_TEMPO_DE_EXPIRACAO)
    to_encode = {"exp": expire, "sub": str(subject), "role": str(role)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITMO)
    return encoded_jwt