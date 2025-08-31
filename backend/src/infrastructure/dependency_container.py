from .external.nltk_text_processor import NLTKTextProcessor
from .external.gemini_ai_service import GeminiAIService
from .parsers.file_parser_factory import FileParserFactory
from ..application.use_cases.process_email_use_case import ProcessEmailUseCase
from ..presentation.controllers.email_controller import EmailController


class DependencyContainer:
    """Container de dependências para injeção de dependência"""
    
    def __init__(self, gemini_api_key: str):
        try:
            # Infraestrutura
            print("🔧 Inicializando processador de texto...")
            self._text_processor = NLTKTextProcessor()
            
            print("🤖 Inicializando serviço de IA...")
            self._ai_service = GeminiAIService(gemini_api_key)
            
            print("📁 Inicializando parser de arquivos...")
            self._file_parser_factory = FileParserFactory()
            
            # Casos de uso
            print("⚙️ Configurando casos de uso...")
            self._process_email_use_case = ProcessEmailUseCase(
                text_processor=self._text_processor,
                ai_service=self._ai_service,
                file_parser_factory=self._file_parser_factory
            )
            
            # Controllers
            print("🎮 Configurando controllers...")
            self._email_controller = EmailController(
                process_email_use_case=self._process_email_use_case,
                text_processor=self._text_processor,
                file_parser_factory=self._file_parser_factory
            )
            print("✅ Container de dependências inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar container: {e}")
            raise RuntimeError(f"Falha na inicialização do container: {e}")
    
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
