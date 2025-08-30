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
    version="2.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Injeta o controller
email_controller = container.email_controller


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
    return await email_controller.process_email(body, subject, file)


@app.post("/extract-text", summary="Extrai texto de arquivos")
async def extract_text(file: UploadFile = File(...)):
    """
    Endpoint para testar extração de texto de arquivos.
    """
    return await email_controller.extract_text_from_file(file)


@app.post("/preprocess", summary="Testa pré-processamento de texto")
async def preprocess_text(body: str = Form(...)):
    """
    Endpoint para testar apenas o pré-processamento do texto.
    """
    return email_controller.preprocess_text(body)


@app.get("/health", summary="Health check da API")
async def health_check():
    """
    Endpoint de health check.
    """
    return email_controller.health_check()


# Mantém endpoints de debug para compatibilidade
@app.post("/debug-eml", summary="Debug específico para arquivos EML")
async def debug_eml(file: UploadFile = File(...)):
    """
    Endpoint para debug específico de arquivos EML.
    """
    return await email_controller.extract_text_from_file(file)


@app.post("/test", summary="Teste simples da API")
async def test_endpoint():
    """
    Endpoint de teste simples.
    """
    return email_controller.health_check()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
