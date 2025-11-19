from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_ORIGINS: str = '["http://localhost:3000","http://192.168.1.10:3000"]'
    
    # App
    PROJECT_NAME: str = "Sistema Clínico Dra. García"
    VERSION: str = "1.0.0"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parsear ALLOWED_ORIGINS de string JSON a lista"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return json.loads(self.ALLOWED_ORIGINS)
        return self.ALLOWED_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()