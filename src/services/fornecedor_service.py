from sqlalchemy.orm import Session

from src.errors.errors import FornecedorError
from src.models.fornecedor import Fornecedor
from src.repositories.fornecedor_repository import (
    buscar_fornecedor_por_id,
    buscar_fornecedores,
    criar_fornecedor,
    deletar_fornecedor,
    editar_fornecedor,
)
from src.repositories.produto_repository import buscar_produtos_por_fornecedores
from src.schemas.fornecedor_schema import FornecedorCreateSucess


def criar_fornecedor_service(db: Session, nome: str) -> FornecedorCreateSucess:
    criar_fornecedor(db=db, nome=nome)
    return FornecedorCreateSucess(message="Fornecedor criado com sucesso.")


def buscar_fornecedores_service(db: Session) -> list[Fornecedor]:
    return buscar_fornecedores(db)


def buscar_fornecedor_por_id_service(db: Session, fornecedor_id: int) -> Fornecedor:
    fornecedor = buscar_fornecedor_por_id(db, fornecedor_id)
    if fornecedor is None:
        raise FornecedorError(
            "SUPPLIER_NOT_FOUND",
            "O fornecedor informado não foi encontrado.",
            {"field": "fornecedor_id", "rule": "supplier_not_found"},
        )
    return fornecedor


def editar_fornecedor_service(
    db: Session,
    fornecedor_id: int,
    nome: str,
) -> Fornecedor:
    buscar_fornecedor_por_id_service(db, fornecedor_id)
    return editar_fornecedor(db=db, fornecedor_id=fornecedor_id, nome=nome)


def deletar_fornecedor_service(db: Session, fornecedor_id: int) -> None:
    buscar_fornecedor_por_id_service(db, fornecedor_id)
    if buscar_produtos_por_fornecedores(db, [fornecedor_id]):
        raise FornecedorError(
            "SUPPLIER_HAS_PRODUCTS",
            "Não é possível excluir um fornecedor associado a produtos.",
            {"field": "fornecedor_id", "rule": "supplier_has_products"},
        )
    deletar_fornecedor(db=db, fornecedor_id=fornecedor_id)
