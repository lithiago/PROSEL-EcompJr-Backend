from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from src.models.usuario import UserRole


class UserRegisterRequest(BaseModel):
    nome: str = Field(...)
    email: str = Field(..., max_length=255)
    senha: str = Field(..., min_length=8, max_length=128)


class UserUpdateRequest(BaseModel):
    nome: str = Field(..., min_length=1)
    email: str = Field(..., min_length=1, max_length=255)


class UserRegisterSucess(BaseModel):
    message: str


class UserAuthRequest(BaseModel):
    email: str = Field(...)
    senha: str = Field(...)


class UserAuthSucess(BaseModel):
    message: str
    id: int
    token: str
    role: str


class UserReadSucess(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    role: UserRole