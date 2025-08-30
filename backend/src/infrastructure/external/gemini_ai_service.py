import json
import google.generativeai as genai
from typing import Optional

from ...domain.services.interfaces import AIServiceInterface
from ...domain.entities.email import Email, EmailAnalysisResult, EmailCategory, ProcessedText


class GeminiAIService(AIServiceInterface):
    """Serviço de IA usando Google Gemini"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel(model_name)
    
    async def analyze_email(self, email: Email, processed_text: ProcessedText) -> EmailAnalysisResult:
        """Analisa um email e gera uma resposta apropriada"""
        try:
            prompt = self._build_analysis_prompt(email, processed_text)
            response = self._model.generate_content(prompt)
            
            return self._parse_response(response.text)
            
        except Exception as e:
            return EmailAnalysisResult(
                category=EmailCategory.PRODUCTIVE,  # Default seguro
                response="Desculpe, ocorreu um erro interno. Tente novamente mais tarde.",
                error=str(e)
            )
    
    def _build_analysis_prompt(self, email: Email, processed_text: ProcessedText) -> str:
        """Constrói o prompt para análise do email"""
        return f"""
        Analise o seguinte email e execute as seguintes tarefas:

        1. Classifique como 'Produtivo' ou 'Improdutivo'
        2. Gere uma resposta automática adequada à categoria:
           - Se PRODUTIVO: resposta que facilita o diálogo e encoraja comunicação
           - Se IMPRODUTIVO: resposta educada mas que desencoraja continuidade

        Email (pré-processado): {processed_text.processed}
        Email original (para contexto): {email.get_full_content()}

        Responda OBRIGATORIAMENTE no seguinte formato JSON:
        {{
            "categoria": "Produtivo" ou "Improdutivo",
            "resposta": "texto da resposta adequada à categoria"
        }}

        DIRETRIZES para respostas:
        - PRODUTIVO: Seja receptivo, ofereça ajuda, peça mais detalhes se necessário
        - IMPRODUTIVO: Seja educado mas firme, redirecione ou encerre gentilmente
        - Todas as respostas devem ser profissionais
        - Responda APENAS o JSON, sem texto adicional
        """
    
    def _parse_response(self, response_text: str) -> EmailAnalysisResult:
        """Faz parse da resposta da IA"""
        try:
            cleaned_response = self._clean_response_text(response_text)
            result = json.loads(cleaned_response)
            
            category = self._parse_category(result.get("categoria", ""))
            response = result.get("resposta", "")
            
            return EmailAnalysisResult(category=category, response=response)
            
        except json.JSONDecodeError as e:
            return EmailAnalysisResult(
                category=EmailCategory.PRODUCTIVE,
                response="Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde.",
                error=f"Erro JSON: {str(e)}"
            )
    
    def _clean_response_text(self, response_text: str) -> str:
        """Remove markdown code blocks da resposta"""
        cleaned = response_text.strip()
        
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]
            
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
            
        return cleaned.strip()
    
    def _parse_category(self, category_str: str) -> EmailCategory:
        """Converte string de categoria para enum"""
        if category_str.lower() in ["produtivo", "productive"]:
            return EmailCategory.PRODUCTIVE
        return EmailCategory.UNPRODUCTIVE
