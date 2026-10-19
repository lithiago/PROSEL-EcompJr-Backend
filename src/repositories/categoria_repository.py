from sqlalchemy.orm import Session

from src.errors.errors import CategoriaError
from src.models.categoria import Categoria


def buscar_categorias(db: Session) -> list[Categoria]:
    return db.query(Categoria).all()


def buscar_categorias_por_id(db: Session, categoria_id: int) -> Categoria | None:
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()


def criar_categoria(db: Session, nome: str) -> Categoria:
    categoria = Categoria(nome=nome)
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


def editar_categoria(db: Session, categoria_id: int, nome: str) -> Categoria:
    categoria = buscar_categorias_por_id(db, categoria_id)
    if categoria is None:
        raise CategoriaError(
            "CATEGORY_NOT_FOUND",
            "A categoria informada não foi encontrada.",
            {"field": "categoria_id", "rule": "category_not_found"},
        )

    categoria.nome = nome
    db.commit()
    db.refresh(categoria)
    return categoria


def deletar_categoria(db: Session, categoria_id: int) -> None:
    categoria = buscar_categorias_por_id(db, categoria_id)
    if categoria is None:
        raise CategoriaError(
            "CATEGORY_NOT_FOUND",
            "A categoria informada não foi encontrada.",
            {"field": "categoria_id", "rule": "category_not_found"},
        )

    db.delete(categoria)
    db.commit()
