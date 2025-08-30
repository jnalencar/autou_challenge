class TextParser:
    """Parser para arquivos de texto"""
    
    def can_parse(self, filename: str) -> bool:
        """Verifica se pode fazer parse de arquivos de texto"""
        return filename.lower().endswith(('.txt', '.text'))
    
    def parse(self, file_content: bytes) -> str:
        """Extrai texto de um arquivo de texto"""
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            try:
                return file_content.decode('latin-1', errors='ignore')
            except Exception as e:
                return f"Erro ao decodificar arquivo de texto: {str(e)}"
