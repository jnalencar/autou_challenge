import time
from typing import Dict, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware de segurança personalizado"""
    
    def __init__(self, app):
        super().__init__(app)
        self.request_counts: Dict[str, Dict[str, int]] = {}
    
    async def dispatch(self, request: Request, call_next):
        """Processa requisições aplicando verificações de segurança"""
        
        # 1. Verifica tamanho do corpo da requisição
        if hasattr(request, 'content_length') and request.content_length:
            if request.content_length > 50 * 1024 * 1024:  # 50MB
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="Arquivo muito grande"
                )
        
        # 2. Headers de segurança
        response = await call_next(request)
        
        # Adiciona headers de segurança
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response

class FileSecurityValidator:
    """Validador de segurança para arquivos"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.eml', '.txt', '.text'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Assinaturas de arquivo para validação
    FILE_SIGNATURES = {
        b'%PDF': '.pdf',
        b'Return-Path:': '.eml',
        b'Received:': '.eml',
        b'From:': '.eml',
    }
    
    @classmethod
    def validate_file(cls, filename: str, content: bytes) -> bool:
        """Valida se o arquivo é seguro"""
        
        # 1. Verifica extensão
        if not cls._is_allowed_extension(filename):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo de arquivo não permitido. Permitidos: {', '.join(cls.ALLOWED_EXTENSIONS)}"
            )
        
        # 2. Verifica tamanho
        if len(content) > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Arquivo muito grande. Máximo: {cls.MAX_FILE_SIZE // 1024 // 1024}MB"
            )
        
        # 3. Verifica assinatura do arquivo
        if not cls._validate_file_signature(filename, content):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Arquivo corrompido ou tipo não corresponde à extensão"
            )
        
        return True
    
    @classmethod
    def _is_allowed_extension(cls, filename: str) -> bool:
        """Verifica se a extensão é permitida"""
        extension = '.' + filename.lower().split('.')[-1] if '.' in filename else ''
        return extension in cls.ALLOWED_EXTENSIONS
    
    @classmethod
    def _validate_file_signature(cls, filename: str, content: bytes) -> bool:
        """Valida a assinatura do arquivo"""
        if len(content) < 10:
            return False
        
        # Para PDFs
        if filename.lower().endswith('.pdf'):
            return content.startswith(b'%PDF')
        
        # Para arquivos de texto
        if filename.lower().endswith(('.txt', '.text')):
            try:
                content.decode('utf-8')
                return True
            except UnicodeDecodeError:
                try:
                    content.decode('latin-1')
                    return True
                except UnicodeDecodeError:
                    return False
        
        # Para emails
        if filename.lower().endswith('.eml'):
            content_str = content[:1000].decode('utf-8', errors='ignore').lower()
            email_indicators = ['return-path:', 'received:', 'from:', 'to:', 'subject:', 'message-id:']
            return any(indicator in content_str for indicator in email_indicators)
        
        return True

def rate_limit_exceeded_handler(request: Request, exc: Exception):
    """Handler personalizado para rate limit excedido"""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit excedido",
            "detail": "Muitas requisições. Tente novamente mais tarde.",
            "retry_after": 60
        }
    )
