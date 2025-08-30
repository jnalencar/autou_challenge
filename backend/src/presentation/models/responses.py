from pydantic import BaseModel
from typing import Optional


class EmailRequest(BaseModel):
    """Modelo de requisição para processamento de email"""
    body: str = ""
    subject: str = ""


class EmailResponse(BaseModel):
    """Modelo de resposta do processamento de email"""
    categoria: str
    resposta: str
    erro: Optional[str] = None


class FileUploadResponse(BaseModel):
    """Resposta para upload de arquivo"""
    filename: str
    content_type: Optional[str]
    extracted_text: str
    text_length: int
    extraction_success: bool
    status: str


class PreprocessResponse(BaseModel):
    """Resposta do pré-processamento de texto"""
    original: str
    processed: str
    token_reduction: str
    status: str


class HealthResponse(BaseModel):
    """Resposta do health check"""
    message: str
    status: str
