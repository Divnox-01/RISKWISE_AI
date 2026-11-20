import os

class Settings:
    PROJECT_NAME: str = "RISKWISE AI 2.0"
    VERSION: str = "2.0.0"
    API_PREFIX: str = "/api"
    
    SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "riskwise-ai-super-secret-key-2026-production-grade")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./riskwise.db")
    ARTIFACTS_DIR: str = os.getenv("ARTIFACTS_DIR", "backend/artifacts")
    
    CORS_ORIGINS: list = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]

settings = Settings()
