
# src/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_TEMPO_DE_EXPIRACAO = 30
JWT_ALGORITMO = "HS256"