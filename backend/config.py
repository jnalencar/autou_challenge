import os
from dotenv import load_dotenv
from typing import List, Optional

# Carrega variáveis do arquivo .env
load_dotenv()

class SecurityConfig:
    """Configurações de segurança"""
    SECRET_KEY: str = os.getenv("SECRET_KEY", "insecure-default-key")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "insecure-jwt-key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

class APIConfig:
    """Configurações da API"""
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    HOST: str = os.getenv("API_HOST", "127.0.0.1")
    PORT: int = int(os.getenv("API_PORT", "8000"))
    RELOAD: bool = os.getenv("API_RELOAD", "True").lower() == "true"

class CORSConfig:
    """Configurações de CORS"""
    ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")
    CREDENTIALS: bool = os.getenv("CORS_CREDENTIALS", "true").lower() == "true"
    METHODS: List[str] = os.getenv("CORS_METHODS", "*").split(",")
    HEADERS: List[str] = os.getenv("CORS_HEADERS", "*").split(",")

class RateLimitConfig:
    """Configurações de rate limiting"""
    CALLS: int = int(os.getenv("RATE_LIMIT_CALLS", "60"))
    PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))

class FileConfig:
    """Configurações de upload de arquivos"""
    MAX_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    ALLOWED_TYPES: List[str] = os.getenv("ALLOWED_FILE_TYPES", ".pdf,.eml,.txt,.text").split(",")

class ProcessingConfig:
    """Configurações de processamento"""
    MIN_CONTENT_LENGTH: int = int(os.getenv("MIN_CONTENT_LENGTH", "10"))
    MIN_WORD_LENGTH: int = int(os.getenv("MIN_WORD_LENGTH", "2"))
    MAX_CONTENT_LENGTH: int = int(os.getenv("MAX_CONTENT_LENGTH", "1000000"))

# Validação de configurações críticas
def validate_config():
    """Valida se as configurações essenciais estão presentes"""
    errors = []
    
    if not APIConfig.GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY não configurada")
    
    if SecurityConfig.SECRET_KEY == "insecure-default-key":
        errors.append("SECRET_KEY usando valor padrão inseguro")
    
    if SecurityConfig.JWT_SECRET_KEY == "insecure-jwt-key":
        errors.append("JWT_SECRET_KEY usando valor padrão inseguro")
    
    if errors:
        raise ValueError(f"Configurações inseguras detectadas: {', '.join(errors)}")

# Configurações consolidadas
security = SecurityConfig()
api = APIConfig()
cors = CORSConfig()
rate_limit = RateLimitConfig()
file_config = FileConfig()
processing = ProcessingConfig()
