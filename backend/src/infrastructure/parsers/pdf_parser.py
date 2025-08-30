import io
from PyPDF2 import PdfReader


class PDFParser:
    """Parser para arquivos PDF"""
    
    def can_parse(self, filename: str) -> bool:
        """Verifica se pode fazer parse de arquivos PDF"""
        return filename.lower().endswith('.pdf')
    
    def parse(self, file_content: bytes) -> str:
        """Extrai texto de um arquivo PDF"""
        try:
            pdf_reader = PdfReader(io.BytesIO(file_content))
            text_parts = []
            
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            text = "\n".join(text_parts).strip()
            
            if len(text) < 10:
                return f"PDF processado mas pouco texto encontrado: '{text[:50]}...'"
            
            return text
            
        except Exception as e:
            return f"Erro ao extrair texto do PDF: {str(e)}"
