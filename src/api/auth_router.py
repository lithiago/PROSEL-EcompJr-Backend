from __future__ import annotations

from datetime import date, datetime, time

from sqlalchemy.orm import Session


from src.services.auth_service import login_service
from src.errors.errors import LoginError, RegisterError
from src.database import SessionLocal
from fastapi import APIRouter, HTTPException, Query, Request, Response, Depends
from fastapi.responses import FileResponse
from sqlalchemy import text

from src.schemas.usuario_schema import UserAuthRequest, UserAuthSucess, UserRegisterRequest, UserRegisterSucess
from src.services.usuario_service import criar_usuario_service

auth_router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@auth_router.post("/register", response_model=UserRegisterSucess, status_code=200)
def criar_usuario(
    payload: UserRegisterRequest, request: Request, db: Session = Depends(get_db)
):
    try:
        return criar_usuario_service(db, payload)
    except RegisterError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )


@auth_router.post("/login", response_model=UserAuthSucess, status_code=200)
def fazer_login(payload: UserAuthRequest, request: Request, db: Session = Depends(get_db)):
    try:
        return login_service(db, payload.email, payload.senha)
    except LoginError as exc:
        raise HTTPException(
            status_code=exc.status_code,
            detail={
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
        )

