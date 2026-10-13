from sqlalchemy.orm import Session
from src.errors.errors import RegisterError
from src.utils.auth_rules import get_senha_hash, validar_senha
from src.schemas.usuario_schema import UserRegisterRequest, UserRegisterSucess
from src.repositories.usuario_respository import buscar_por_email, criar_usuario

# def obter_usuario_por_email(db: Session, email: str):
#     usuario = buscar_por_email(db, email)
#     return usuario


def criar_usuario_service(
    db: Session, usuario: UserRegisterRequest
) -> UserRegisterSucess:
    validar_senha(usuario.senha)
    if buscar_por_email(db, usuario.email):
        raise RegisterError(
            "EMAIL_IN_USE",
            "O E-mail informado já está cadastrado.",
            {
                "field": "email",
                "rule": "email_in_use",
            },
        )

    try:
        hash = get_senha_hash(usuario.senha)
    except ValueError as exc:
        raise RegisterError(
            "INVALID_PASSWORD",
            "Nao foi possivel processar a senha informada.",
            {"field": "password", "reason": "hash_error"},
        ) from exc

    criar_usuario(
        db=db,
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=hash,
    )
    return UserRegisterSucess(message="Usuário criado com sucesso.")
