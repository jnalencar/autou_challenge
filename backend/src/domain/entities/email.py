from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EmailCategory(Enum):
    PRODUCTIVE = "Produtivo"
    UNPRODUCTIVE = "Improdutivo"


@dataclass
class Email:
    """Entidade que representa um email"""
    content: str
    subject: Optional[str] = None
    sender: Optional[str] = None
    
    def is_valid(self) -> bool:
        """Verifica se o email tem conteúdo válido"""
        return bool(self.content and len(self.content.strip()) >= 10)
    
    def get_full_content(self) -> str:
        """Retorna o conteúdo completo do email formatado"""
        parts = []
        
        if self.subject:
            parts.append(f"Assunto: {self.subject}")
        
        if self.sender:
            parts.append(f"De: {self.sender}")
            
        if parts:
            parts.append("")  # Linha em branco
            
        parts.append(self.content)
        
        return "\n".join(parts)


@dataclass
class ProcessedText:
    """Representa um texto processado"""
    original: str
    processed: str
    
    def get_token_reduction_info(self) -> str:
        """Calcula a redução de tokens"""
        original_words = len(self.original.split())
        processed_words = len(self.processed.split())
        return f"{original_words} -> {processed_words} palavras"


@dataclass
class EmailAnalysisResult:
    """Resultado da análise de um email"""
    category: EmailCategory
    response: str
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Converte o resultado para dicionário"""
        result = {
            "categoria": self.category.value,
            "resposta": self.response
        }
        
        if self.error:
            result["erro"] = self.error
            
        return result
