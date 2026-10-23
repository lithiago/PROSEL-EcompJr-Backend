from sqlalchemy.orm import Session
from src.models.usuario import Usuario


def listar_usuarios(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def buscar_por_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def buscar_por_email(db: Session, email: str):
    return(
        db.query(Usuario).filter(Usuario.email == email).first()
    )


def criar_usuario(db: Session, nome: str, email:str, senha_hash: str):
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    return usuario


def atualizar_usuario(
    db: Session,
    usuario: Usuario,
    nome: str,
    email: str,
) -> Usuario:
    usuario.nome = nome
    usuario.email = email
    db.commit()
    db.refresh(usuario)
    return usuario


def deletar_usuario(db: Session, usuario: Usuario) -> None:
    db.delete(usuario)
    db.commit()