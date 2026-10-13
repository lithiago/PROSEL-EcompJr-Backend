from sqlalchemy.orm import Session
from src.models.usuario import Usuario


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