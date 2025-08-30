from dataclasses import dataclass
from typing import Optional


@dataclass
class FileInfo:
    """Informações sobre um arquivo"""
    filename: str
    content_type: Optional[str]
    size: int
    
    def get_extension(self) -> str:
        """Retorna a extensão do arquivo"""
        return self.filename.lower().split('.')[-1] if '.' in self.filename else ""
    
    def is_pdf(self) -> bool:
        """Verifica se é um arquivo PDF"""
        return self.get_extension() == "pdf"
    
    def is_eml(self) -> bool:
        """Verifica se é um arquivo EML"""
        return self.get_extension() == "eml"
    
    def is_text(self) -> bool:
        """Verifica se é um arquivo de texto"""
        return self.get_extension() in ["txt", "text"]
