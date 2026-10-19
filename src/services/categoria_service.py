from sqlalchemy.orm import Session

from src.errors.errors import CategoriaError
from src.models.categoria import Categoria
from src.repositories.categoria_repository import (
    buscar_categorias,
    buscar_categorias_por_id,
    criar_categoria,
    deletar_categoria,
    editar_categoria,
)


def criar_categoria_service(db: Session, nome: str) -> Categoria:
    return criar_categoria(db=db, nome=nome)


def buscar_categorias_service(db: Session) -> list[Categoria]:
    return buscar_categorias(db)


def buscar_categoria_por_id_service(db: Session, categoria_id: int) -> Categoria:
    categoria = buscar_categorias_por_id(db, categoria_id)
    if categoria is None:
        raise CategoriaError(
            "CATEGORY_NOT_FOUND",
            "A categoria informada não foi encontrada.",
            {"field": "categoria_id", "rule": "category_not_found"},
        )
    return categoria


def editar_categoria_service(
    db: Session,
    categoria_id: int,
    nome: str,
) -> Categoria:
    buscar_categoria_por_id_service(db, categoria_id)
    return editar_categoria(db=db, categoria_id=categoria_id, nome=nome)


def deletar_categoria_service(db: Session, categoria_id: int) -> None:
    buscar_categoria_por_id_service(db, categoria_id)
    deletar_categoria(db=db, categoria_id=categoria_id)
