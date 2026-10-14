from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ApiError(Exception):
    code: str
    message: str
    status_code: int
    details: dict[str, Any] = field(default_factory=dict)


class RegisterError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(code=code, message=message, status_code=422, details=details or {})

class LoginError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
            super().__init__(code=code, message=message, status_code=401, details=details or {})
class ProdutoError(ApiError):
    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(code=code, message=message, status_code=422, details=details or {})
        
        
