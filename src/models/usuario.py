from enum import Enum

from sqlalchemy import Column, Enum as SQLEnum, Integer, String
from sqlalchemy.orm import DeclarativeBase
from .base import Base


class UserRole(str, Enum):
    OPERADOR = "OPERADOR"
    ADMIN = "ADMINISTRADOR"


class Usuario(Base):
    __tablename__ = "Usuario"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    senha_hash = Column(String, nullable=False)
    role = Column(
        SQLEnum(UserRole),
        nullable=False,
        default=UserRole.OPERADOR,
        index=True
    )