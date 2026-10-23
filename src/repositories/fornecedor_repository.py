from sqlalchemy.orm import Session

from src.errors.errors import FornecedorError
from src.models.fornecedor import Fornecedor


def buscar_fornecedores(db: Session) -> list[Fornecedor]:
    return db.query(Fornecedor).all()


def buscar_fornecedor_por_id(db: Session, fornecedor_id: int) -> Fornecedor | None:
    return db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()


def criar_fornecedor(db: Session, nome: str) -> Fornecedor:
    fornecedor = Fornecedor(nome=nome)
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor


def editar_fornecedor(db: Session, fornecedor_id: int, nome: str) -> Fornecedor:
    fornecedor = buscar_fornecedor_por_id(db, fornecedor_id)
    if fornecedor is None:
        raise FornecedorError(
            "SUPPLIER_NOT_FOUND",
            "O fornecedor informado não foi encontrado.",
            {"field": "fornecedor_id", "rule": "supplier_not_found"},
        )

    fornecedor.nome = nome
    db.commit()
    db.refresh(fornecedor)
    return fornecedor


def deletar_fornecedor(db: Session, fornecedor_id: int) -> None:
    fornecedor = buscar_fornecedor_por_id(db, fornecedor_id)
    if fornecedor is None:
        raise FornecedorError(
            "SUPPLIER_NOT_FOUND",
            "O fornecedor informado não foi encontrado.",
            {"field": "fornecedor_id", "rule": "supplier_not_found"},
        )

    db.delete(fornecedor)
    db.commit()
