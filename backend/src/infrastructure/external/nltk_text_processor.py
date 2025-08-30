import nltk
import re
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

from ...domain.services.interfaces import TextProcessorInterface
from ...domain.entities.email import ProcessedText


class NLTKTextProcessor(TextProcessorInterface):
    """Processador de texto usando NLTK"""
    
    def __init__(self):
        self._stemmer = RSLPStemmer()
        self._ensure_nltk_resources()
    
    def preprocess_text(self, text: str) -> ProcessedText:
        """
        Pré-processa o texto seguindo as etapas:
        - Remove acentos
        - Converte para minúsculas
        - Remove pontuação e números
        - Remove stop words
        - Aplica stemming
        """
        original_text = text
        
        # Remove acentos
        processed = unidecode(text)
        
        # Converte para minúsculas
        processed = processed.lower()
        
        # Remove pontuação e números
        processed = re.sub(r'[^\w\s]', '', processed)
        processed = re.sub(r'\d+', '', processed)
        
        # Tokeniza o texto
        words = nltk.word_tokenize(processed, language='portuguese')
        
        # Remove stop words em português
        stop_words = set(stopwords.words('portuguese'))
        words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Aplica stemming
        words = [self._stemmer.stem(word) for word in words]
        
        # Reconstrói o texto
        processed_text = ' '.join(words)
        
        return ProcessedText(original=original_text, processed=processed_text)
    
    def _ensure_nltk_resources(self):
        """Garante que os recursos do NLTK estão disponíveis"""
        resources = [
            ('tokenizers/punkt_tab', 'punkt_tab'),
            ('corpora/stopwords', 'stopwords'),
            ('stemmers/rslp', 'rslp')
        ]
        
        for resource_path, resource_name in resources:
            try:
                nltk.data.find(resource_path)
            except LookupError:
                nltk.download(resource_name)
