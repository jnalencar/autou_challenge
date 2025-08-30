from typing import Optional
from fastapi import UploadFile

from ...domain.entities.email import Email, EmailAnalysisResult, EmailCategory
from ...domain.entities.file import FileInfo
from ...domain.services.interfaces import TextProcessorInterface, AIServiceInterface
from ...infrastructure.parsers.file_parser_factory import FileParserFactory


class ProcessEmailUseCase:
    """Caso de uso para processamento de emails"""
    
    def __init__(
        self,
        text_processor: TextProcessorInterface,
        ai_service: AIServiceInterface,
        file_parser_factory: FileParserFactory
    ):
        self._text_processor = text_processor
        self._ai_service = ai_service
        self._file_parser_factory = file_parser_factory
    
    async def execute(
        self,
        body: str = "",
        subject: str = "",
        file: Optional[UploadFile] = None
    ) -> EmailAnalysisResult:
        """Executa o processamento completo do email"""
        
        # 1. Extrai conteúdo do arquivo ou usa o body
        content = await self._extract_content(file, body)
        
        # 2. Cria a entidade Email
        email = Email(content=content, subject=subject if subject.strip() else None)
        
        # 3. Valida se o email tem conteúdo suficiente
        if not email.is_valid():
            return EmailAnalysisResult(
                category=EmailCategory.PRODUCTIVE,  # Default seguro
                response="Nenhum conteúdo fornecido. Envie um texto ou arquivo com conteúdo válido.",
                error="Conteúdo insuficiente"
            )
        
        # 4. Pré-processa o texto
        processed_text = self._text_processor.preprocess_text(email.get_full_content())
        
        # 5. Analisa com IA
        result = await self._ai_service.analyze_email(email, processed_text)
        
        return result
    
    async def _extract_content(self, file: Optional[UploadFile], body: str) -> str:
        """Extrai conteúdo do arquivo ou retorna o body"""
        if file and file.filename:
            return await self._extract_from_file(file)
        
        return body.strip()
    
    async def _extract_from_file(self, file: UploadFile) -> str:
        """Extrai conteúdo de um arquivo"""
        try:
            file_content = await file.read()
            await file.seek(0)  # Reset file pointer
            
            file_info = FileInfo(
                filename=file.filename or "",
                content_type=file.content_type,
                size=len(file_content)
            )
            
            return self._file_parser_factory.parse_file(file_content, file_info)
            
        except Exception as e:
            return f"Erro ao processar arquivo {file.filename}: {str(e)}"
