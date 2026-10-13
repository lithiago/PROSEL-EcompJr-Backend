from sqlalchemy.orm import Session

from src.schemas.usuario_schema import UserAuthSucess
from src.errors.errors import LoginError
from src.repositories.usuario_respository import buscar_por_email
from src.utils.auth_rules import comparar_senhas, create_access_token





def login_service(db: Session, email: str, senha: str):
    usuario = buscar_por_email(db, email)

    if not usuario:
        raise LoginError(
            "INVALID_CREDENTIALS",
            "E-mail ou senha inválidos."
        )

    if not comparar_senhas(senha, usuario.senha_hash):
        raise LoginError(
            "INVALID_CREDENTIALS",
            "E-mail ou senha inválidos."
        )
    token = create_access_token(usuario.id, usuario.role)

    return UserAuthSucess(
        message="Login bem sucedido",
        token=token,
        id=usuario.id,
        role=usuario.role
    )