from .external.nltk_text_processor import NLTKTextProcessor
from .external.gemini_ai_service import GeminiAIService
from .parsers.file_parser_factory import FileParserFactory
from ..application.use_cases.process_email_use_case import ProcessEmailUseCase
from ..presentation.controllers.email_controller import EmailController


class DependencyContainer:
    """Container de dependências para injeção de dependência"""
    
    def __init__(self, gemini_api_key: str):
        # Infraestrutura
        self._text_processor = NLTKTextProcessor()
        self._ai_service = GeminiAIService(gemini_api_key)
        self._file_parser_factory = FileParserFactory()
        
        # Casos de uso
        self._process_email_use_case = ProcessEmailUseCase(
            text_processor=self._text_processor,
            ai_service=self._ai_service,
            file_parser_factory=self._file_parser_factory
        )
        
        # Controllers
        self._email_controller = EmailController(
            process_email_use_case=self._process_email_use_case,
            text_processor=self._text_processor,
            file_parser_factory=self._file_parser_factory
        )
    
    @property
    def email_controller(self) -> EmailController:
        """Retorna o controller de email"""
        return self._email_controller
    
    @property
    def text_processor(self) -> NLTKTextProcessor:
        """Retorna o processador de texto"""
        return self._text_processor
    
    @property
    def file_parser_factory(self) -> FileParserFactory:
        """Retorna a factory de parsers"""
        return self._file_parser_factory
