from sqlalchemy.orm import Session

from src.errors.errors import RegisterError, UsuarioError
from src.schemas.usuario_schema import (
    UserReadSucess,
    UserRegisterRequest,
    UserRegisterSucess,
    UserUpdateRequest,
)
from src.repositories.usuario_respository import (
    atualizar_usuario,
    buscar_por_id,
    buscar_por_email,
    criar_usuario,
    deletar_usuario,
    listar_usuarios,
)
from src.utils.auth_rules import get_senha_hash, validar_senha

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


def get_usuarios_service(db: Session) -> list[UserReadSucess]:
    return [
        UserReadSucess.model_validate(usuario)
        for usuario in listar_usuarios(db)
    ]


def get_usuario_por_id_service(db: Session, usuario_id: int) -> UserReadSucess:
    usuario = buscar_por_id(db, usuario_id)
    if usuario is None:
        raise UsuarioError(
            "USER_NOT_FOUND",
            "O usuário informado não foi encontrado.",
            {"field": "usuario_id", "rule": "user_not_found"},
        )
    return UserReadSucess.model_validate(usuario)


def editar_usuario_service(
    db: Session,
    usuario_id: int,
    payload: UserUpdateRequest,
) -> UserReadSucess:
    usuario = buscar_por_id(db, usuario_id)
    if usuario is None:
        raise UsuarioError(
            "USER_NOT_FOUND",
            "O usuário informado não foi encontrado.",
            {"field": "usuario_id", "rule": "user_not_found"},
        )

    usuario_com_email = buscar_por_email(db, payload.email)
    if usuario_com_email is not None and usuario_com_email.id != usuario_id:
        raise UsuarioError(
            "EMAIL_IN_USE",
            "O E-mail informado já está cadastrado.",
            {"field": "email", "rule": "email_in_use"},
        )

    usuario_atualizado = atualizar_usuario(
        db=db,
        usuario=usuario,
        nome=payload.nome,
        email=payload.email,
    )
    return UserReadSucess.model_validate(usuario_atualizado)


def deletar_usuario_service(db: Session, usuario_id: int) -> None:
    usuario = buscar_por_id(db, usuario_id)
    if usuario is None:
        raise UsuarioError(
            "USER_NOT_FOUND",
            "O usuário informado não foi encontrado.",
            {"field": "usuario_id", "rule": "user_not_found"},
        )
    deletar_usuario(db, usuario)
