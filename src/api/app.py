from __future__ import annotations

# from api import auth_router
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import inspect, text

# from src.api.errors import ApiError
from src.api.categoria_router import categorias_router
from src.api.produtos_router import produtos_router
from src.api.auth_router import auth_router

app = FastAPI(title="prosel-API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(produtos_router)
app.include_router(categorias_router)
