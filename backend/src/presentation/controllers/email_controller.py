from fastapi import Form, UploadFile, File
from typing import Optional

from ...application.use_cases.process_email_use_case import ProcessEmailUseCase
from ...domain.services.interfaces import TextProcessorInterface
from ...infrastructure.parsers.file_parser_factory import FileParserFactory
from ...domain.entities.file import FileInfo
from ..models.responses import (
    EmailResponse, 
    FileUploadResponse, 
    PreprocessResponse, 
    HealthResponse
)


class EmailController:
    """Controller para endpoints relacionados a email"""
    
    def __init__(
        self, 
        process_email_use_case: ProcessEmailUseCase,
        text_processor: TextProcessorInterface,
        file_parser_factory: FileParserFactory
    ):
        self._process_email_use_case = process_email_use_case
        self._text_processor = text_processor
        self._file_parser_factory = file_parser_factory
    
    async def process_email(
        self, 
        body: str = Form(""), 
        subject: str = Form(""), 
        file: Optional[UploadFile] = File(None)
    ) -> EmailResponse:
        """Processa um email e retorna a análise"""
        try:
            result = await self._process_email_use_case.execute(body, subject, file)
            response_dict = result.to_dict()
            
            return EmailResponse(**response_dict)
            
        except Exception as e:
            return EmailResponse(
                categoria="Erro",
                resposta="Desculpe, ocorreu um erro interno. Tente novamente mais tarde.",
                erro=str(e)
            )
    
    async def extract_text_from_file(self, file: UploadFile = File(...)) -> FileUploadResponse:
        """Extrai texto de um arquivo"""
        try:
            file_content = await file.read()
            await file.seek(0)
            
            file_info = FileInfo(
                filename=file.filename or "",
                content_type=file.content_type,
                size=len(file_content)
            )
            
            extracted_text = self._file_parser_factory.parse_file(file_content, file_info)
            
            return FileUploadResponse(
                filename=file_info.filename,
                content_type=file_info.content_type,
                extracted_text=extracted_text,
                text_length=len(extracted_text),
                extraction_success=not ("Erro" in extracted_text and extracted_text.startswith("Erro")),
                status="success"
            )
            
        except Exception as e:
            return FileUploadResponse(
                filename=file.filename or "unknown",
                content_type=file.content_type,
                extracted_text="",
                text_length=0,
                extraction_success=False,
                status="error"
            )
    
    def preprocess_text(self, body: str = Form(...)) -> PreprocessResponse:
        """Testa o pré-processamento de texto"""
        try:
            processed_text = self._text_processor.preprocess_text(body)
            
            return PreprocessResponse(
                original=processed_text.original,
                processed=processed_text.processed,
                token_reduction=processed_text.get_token_reduction_info(),
                status="success"
            )
            
        except Exception as e:
            return PreprocessResponse(
                original=body,
                processed="",
                token_reduction="",
                status="error"
            )
    
    def health_check(self) -> HealthResponse:
        """Endpoint de health check"""
        return HealthResponse(
            message="API funcionando!",
            status="ok"
        )
