from src.errors.errors import RegisterError
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