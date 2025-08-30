from abc import ABC, abstractmethod
from typing import Protocol

from ..entities.email import Email, EmailAnalysisResult, ProcessedText


class TextProcessorInterface(ABC):
    """Interface para processamento de texto"""
    
    @abstractmethod
    def preprocess_text(self, text: str) -> ProcessedText:
        """Pré-processa o texto removendo stop words e aplicando stemming"""
        pass


class AIServiceInterface(ABC):
    """Interface para serviços de IA"""
    
    @abstractmethod
    async def analyze_email(self, email: Email, processed_text: ProcessedText) -> EmailAnalysisResult:
        """Analisa um email e gera uma resposta"""
        pass


class FileParserInterface(Protocol):
    """Interface para parsers de arquivo"""
    
    def can_parse(self, filename: str) -> bool:
        """Verifica se pode fazer parse do arquivo"""
        ...
    
    def parse(self, file_content: bytes) -> str:
        """Faz parse do conteúdo do arquivo"""
        ...
