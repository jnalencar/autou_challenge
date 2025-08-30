from fastapi import FastAPI, Form, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import os

# Importações da aplicação
from src.infrastructure.dependency_container import DependencyContainer
from src.infrastructure.security.middleware import SecurityMiddleware, FileSecurityValidator
from config import api, cors, security, file_config, validate_config

# Valida configurações de segurança
try:
    validate_config()
except ValueError as e:
    print(f"⚠️  AVISO DE SEGURANÇA: {e}")
    print("Configure adequadamente o arquivo .env antes de usar em produção!")

# Inicializa o container de dependências
container = DependencyContainer(api.GEMINI_API_KEY)

# Cria a aplicação FastAPI
app = FastAPI(
    title="Email Processor API",
    description="API para processamento e análise de emails usando IA",
    version="2.0.0",
    docs_url="/docs" if api.DEBUG else None,  # Desabilita docs em produção
    redoc_url="/redoc" if api.DEBUG else None,  # Desabilita redoc em produção
)

# Adiciona middleware de segurança
app.add_middleware(SecurityMiddleware)

# Configura CORS de forma segura
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors.ORIGINS,
    allow_credentials=cors.CREDENTIALS,
    allow_methods=cors.METHODS,
    allow_headers=cors.HEADERS,
)

# Injeta o controller
email_controller = container.email_controller

# Handler para validação de arquivos
async def validate_uploaded_file(file: UploadFile):
    """Valida arquivo antes do processamento"""
    if file and file.filename:
        content = await file.read()
        await file.seek(0)  # Reset para leitura posterior
        FileSecurityValidator.validate_file(file.filename, content)

# === ENDPOINTS ===

@app.post("/processar", summary="Processa e analisa um email")
async def process_email(
    body: str = Form(""), 
    subject: str = Form(""), 
    file: Optional[UploadFile] = File(None)
):
    """
    Endpoint principal para processamento de emails.
    Aceita texto direto ou arquivos (.txt, .pdf, .eml).
    """
    # Valida arquivo se fornecido
    if file:
        await validate_uploaded_file(file)
    
    return await email_controller.process_email(body, subject, file)


@app.post("/extract-text", summary="Extrai texto de arquivos")
async def extract_text(file: UploadFile = File(...)):
    """
    Endpoint para testar extração de texto de arquivos.
    """
    await validate_uploaded_file(file)
    return await email_controller.extract_text_from_file(file)


@app.post("/preprocess", summary="Testa pré-processamento de texto")
async def preprocess_text(body: str = Form(...)):
    """
    Endpoint para testar apenas o pré-processamento do texto.
    """
    # Valida tamanho do conteúdo
    if len(body) > file_config.MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Conteúdo muito longo"
        )
    
    return email_controller.preprocess_text(body)


@app.get("/health", summary="Health check da API")
async def health_check():
    """
    Endpoint de health check.
    """
    return email_controller.health_check()


# Mantém endpoints de debug para compatibilidade (apenas em desenvolvimento)
if api.DEBUG:
    @app.post("/debug-eml", summary="Debug específico para arquivos EML")
    async def debug_eml(file: UploadFile = File(...)):
        """
        Endpoint para debug específico de arquivos EML.
        """
        await validate_uploaded_file(file)
        return await email_controller.extract_text_from_file(file)

    @app.post("/test", summary="Teste simples da API")
    async def test_endpoint():
        """
        Endpoint de teste simples.
        """
        return email_controller.health_check()


# Handler de erro global
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler personalizado para exceções HTTP"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Erro na requisição",
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handler para exceções gerais"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erro interno do servidor",
            "detail": "Algo deu errado. Tente novamente mais tarde." if not api.DEBUG else str(exc),
            "status_code": 500
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=api.HOST, 
        port=api.PORT, 
        reload=api.RELOAD,
        access_log=api.DEBUG
    )
