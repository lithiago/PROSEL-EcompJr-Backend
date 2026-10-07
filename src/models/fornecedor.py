from sqlalchemy import Column, Integer, String
from .base import Base

class Fornecedor(Base):
    __tablename__ = "Fornecedor"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)