from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserRegisterRequest(BaseModel):
    nome: str = Field(...)
    email: str = Field(..., max_length=255)
    senha: str = Field(..., min_length=8, max_length=128)

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