from typing import List, Optional
from ...domain.entities.file import FileInfo
from .pdf_parser import PDFParser
from .eml_parser import EMLParser
from .text_parser import TextParser


class FileParserFactory:
    """Factory para criação de parsers de arquivo"""
    
    def __init__(self):
        self._parsers = [
            PDFParser(),
            EMLParser(),
            TextParser()
        ]
    
    def get_parser(self, file_info: FileInfo):
        """Retorna o parser apropriado para o arquivo"""
        for parser in self._parsers:
            if parser.can_parse(file_info.filename):
                return parser
        
        return None
    
    def parse_file(self, file_content: bytes, file_info: FileInfo) -> str:
        """Faz parse do arquivo usando o parser apropriado"""
        parser = self.get_parser(file_info)
        
        if parser:
            return parser.parse(file_content)
        
        # Fallback: tenta decodificar como texto
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_content.decode('latin-1', errors='ignore')
            except Exception as e:
                return f"Erro: Tipo de arquivo não suportado ou corrompido. Arquivo: {file_info.filename}, Erro: {str(e)}"
