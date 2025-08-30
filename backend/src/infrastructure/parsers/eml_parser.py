import re


class EMLParser:
    """Parser para arquivos EML (email)"""
    
    def can_parse(self, filename: str) -> bool:
        """Verifica se pode fazer parse de arquivos EML"""
        return filename.lower().endswith('.eml')
    
    def parse(self, file_content: bytes) -> str:
        """Extrai texto de um arquivo EML"""
        try:
            content_str = self._decode_content(file_content)
            
            subject = self._extract_subject(content_str)
            sender = self._extract_sender(content_str)
            body = self._extract_body(content_str)
            
            return self._format_email_content(subject, sender, body)
            
        except Exception as e:
            return self._fallback_extraction(file_content, e)
    
    def _decode_content(self, file_content: bytes) -> str:
        """Decodifica o conteúdo do arquivo"""
        if isinstance(file_content, bytes):
            return file_content.decode('utf-8', errors='ignore')
        return str(file_content)
    
    def _extract_subject(self, content: str) -> str:
        """Extrai o assunto do email"""
        match = re.search(r'Subject:\s*([^\r\n]+)', content, re.IGNORECASE)
        return match.group(1).strip() if match else 'Sem assunto'
    
    def _extract_sender(self, content: str) -> str:
        """Extrai o remetente do email"""
        match = re.search(r'From:\s*([^\r\n]+)', content, re.IGNORECASE)
        return match.group(1).strip() if match else 'Remetente desconhecido'
    
    def _extract_body(self, content: str) -> str:
        """Extrai o corpo do email"""
        # Tenta extrair text/plain primeiro
        body = self._extract_plain_text(content)
        
        if not body:
            # Se não encontrar, tenta HTML
            body = self._extract_html_text(content)
        
        if not body:
            # Fallback: pega tudo após headers
            body = self._extract_fallback_body(content)
        
        return self._clean_body_text(body)
    
    def _extract_plain_text(self, content: str) -> str:
        """Extrai texto plano do email"""
        pattern = r'Content-Type:\s*text/plain.*?\n\n(.*?)(?=--\w+|$)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
    
    def _extract_html_text(self, content: str) -> str:
        """Extrai e limpa texto HTML"""
        pattern = r'Content-Type:\s*text/html.*?\n\n(.*?)(?=--\w+|$)'
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        
        if match:
            html_body = match.group(1).strip()
            # Remove tags HTML
            text = re.sub(r'<[^>]+>', '', html_body)
            text = re.sub(r'&nbsp;', ' ', text)
            text = re.sub(r'&[a-zA-Z0-9]+;', '', text)
            return text
        
        return ""
    
    def _extract_fallback_body(self, content: str) -> str:
        """Extração de fallback quando não encontra content-type específico"""
        header_end = content.find('\n\n')
        if header_end != -1:
            body = content[header_end + 2:].strip()
            # Remove boundaries
            body = re.sub(r'--\w+.*', '', body, flags=re.DOTALL)
            return body
        
        return "Não foi possível extrair o corpo do email"
    
    def _clean_body_text(self, body: str) -> str:
        """Limpa o texto do corpo do email"""
        if not body:
            return ""
        
        # Limpa quoted-printable encoding
        body = re.sub(r'=\r?\n', '', body)
        body = re.sub(r'=([0-9A-F]{2})', lambda m: chr(int(m.group(1), 16)), body)
        
        # Limpa espaços extras
        body = re.sub(r'\n\s*\n', '\n\n', body)
        return body.strip()
    
    def _format_email_content(self, subject: str, sender: str, body: str) -> str:
        """Formata o conteúdo completo do email"""
        return f"Assunto: {subject}\nDe: {sender}\n\n{body}"
    
    def _fallback_extraction(self, file_content: bytes, original_error: Exception) -> str:
        """Extração de fallback em caso de erro"""
        try:
            content_str = self._decode_content(file_content)
            
            # Remove headers técnicos
            content_str = re.sub(r'MIME-Version:.*?\n', '', content_str)
            content_str = re.sub(r'Content-Type:.*?\n', '', content_str)
            content_str = re.sub(r'Content-Transfer-Encoding:.*?\n', '', content_str)
            content_str = re.sub(r'--\w+.*?\n', '', content_str)
            
            return f"Email extraído (método simplificado):\n{content_str.strip()}"
            
        except Exception:
            return f"Conteúdo do arquivo EML (erro na extração: {str(original_error)})"
