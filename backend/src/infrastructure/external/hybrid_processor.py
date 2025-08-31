import re
from unidecode import unidecode
from typing import List, Set
from ...domain.services.interfaces import TextProcessorInterface
from ...domain.entities.email import ProcessedText


class HybridTextProcessor(TextProcessorInterface):
    """Processador híbrido que combina várias técnicas"""
    
    def __init__(self):
        self._setup_resources()
    
    def _setup_resources(self):
        """Configura recursos de processamento"""
        # Stop words expandidas
        self._stop_words = self._get_comprehensive_stopwords()
        
        # Padrões de regex
        self._email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        self._url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        self._phone_pattern = re.compile(r'\b\d{2,3}[-.\s]?\d{4,5}[-.\s]?\d{4}\b')
        
        # Sufixos comuns em português para stemming simples
        self._suffix_rules = [
            ('ando', 'ar'), ('endo', 'er'), ('indo', 'ir'),
            ('ados', 'ar'), ('idos', 'ir'), ('ação', 'ar'),
            ('mente', ''), ('ção', 'r'), ('dade', ''),
            ('ismo', ''), ('ista', ''), ('ável', ''),
            ('ível', ''), ('oso', ''), ('osa', ''),
            ('ado', 'ar'), ('ida', 'ir'), ('ção', 'r')
        ]
    
    def _get_comprehensive_stopwords(self) -> Set[str]:
        """Stop words abrangentes em português"""
        return {
            # Artigos
            'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
            # Preposições
            'de', 'da', 'do', 'das', 'dos', 'em', 'na', 'no', 'nas', 'nos',
            'por', 'para', 'com', 'sem', 'sobre', 'entre', 'até', 'desde',
            'ante', 'após', 'contra', 'durante', 'mediante', 'perante',
            'sob', 'trás', 'diante', 'dentro', 'fora', 'perto', 'longe',
            # Conjunções
            'e', 'ou', 'mas', 'que', 'se', 'como', 'quando', 'onde',
            'porque', 'embora', 'contudo', 'entretanto', 'portanto',
            'todavia', 'porém', 'logo', 'pois', 'assim', 'então',
            # Pronomes
            'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
            'me', 'te', 'se', 'nos', 'vos', 'lhe', 'lhes', 'mim', 'ti',
            'meu', 'minha', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas',
            'seu', 'sua', 'seus', 'suas', 'nosso', 'nossa', 'nossos', 'nossas',
            'vosso', 'vossa', 'vossos', 'vossas',
            'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas',
            'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'isso', 'aquilo',
            'qual', 'quais', 'que', 'quem', 'cujo', 'cuja', 'cujos', 'cujas',
            # Verbos auxiliares e comuns
            'ser', 'estar', 'ter', 'haver', 'ir', 'vir', 'dar', 'fazer', 'dizer',
            'ver', 'saber', 'poder', 'querer', 'ficar', 'chegar', 'passar',
            'é', 'são', 'foi', 'foram', 'era', 'eram', 'seja', 'sejam', 'sendo', 'sido',
            'está', 'estão', 'estava', 'estavam', 'esteja', 'estejam', 'estando', 'estado',
            'tem', 'têm', 'teve', 'tiveram', 'tinha', 'tinham', 'tenha', 'tenham', 'tendo', 'tido',
            'há', 'houve', 'houveram', 'havia', 'haviam', 'haja', 'hajam', 'havendo', 'havido',
            # Advérbios
            'não', 'sim', 'já', 'ainda', 'mais', 'menos', 'muito', 'pouco',
            'bem', 'mal', 'melhor', 'pior', 'sempre', 'nunca', 'jamais',
            'hoje', 'ontem', 'amanhã', 'agora', 'depois', 'antes', 'cedo', 'tarde',
            'aqui', 'ali', 'lá', 'cá', 'aí', 'onde', 'aonde', 'donde',
            'assim', 'também', 'apenas', 'só', 'somente', 'mesmo', 'próprio',
            'talvez', 'quase', 'cerca', 'perto', 'longe', 'dentro', 'fora',
            'acima', 'abaixo', 'bastante', 'demais', 'deveras', 'assaz'
        }
    
    def preprocess_text(self, text: str) -> ProcessedText:
        """Processamento híbrido avançado"""
        original_text = text
        
        # 1. Limpeza inicial
        processed = self._clean_text(text)
        
        # 2. Normalização
        processed = self._normalize_text(processed)
        
        # 3. Tokenização inteligente
        words = self._smart_tokenize(processed)
        
        # 4. Filtragem avançada
        words = self._filter_words(words)
        
        # 5. Stemming simples
        words = self._simple_stem(words)
        
        processed_text = ' '.join(words)
        
        return ProcessedText(original=original_text, processed=processed_text)
    
    def _clean_text(self, text: str) -> str:
        """Limpeza inicial do texto"""
        # Remove emails, URLs e telefones
        text = self._email_pattern.sub(' ', text)
        text = self._url_pattern.sub(' ', text)
        text = self._phone_pattern.sub(' ', text)
        
        # Remove quebras de linha e tabs
        text = re.sub(r'[\n\r\t]+', ' ', text)
        
        return text
    
    def _normalize_text(self, text: str) -> str:
        """Normalização do texto"""
        # Remove acentos
        text = unidecode(text)
        
        # Converte para minúsculas
        text = text.lower()
        
        # Remove pontuação e caracteres especiais
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remove números
        text = re.sub(r'\d+', ' ', text)
        
        # Remove underscores
        text = re.sub(r'_+', ' ', text)
        
        # Normaliza espaços
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def _smart_tokenize(self, text: str) -> List[str]:
        """Tokenização inteligente"""
        # Split básico
        words = text.split()
        
        # Remove palavras com caracteres repetitivos (spam)
        filtered_words = []
        for word in words:
            # Remove palavras com muita repetição de caracteres
            if len(set(word)) <= 2 and len(word) > 4:
                continue
            # Remove palavras muito curtas ou muito longas
            if len(word) < 2 or len(word) > 30:
                continue
            filtered_words.append(word)
        
        return filtered_words
    
    def _filter_words(self, words: List[str]) -> List[str]:
        """Filtragem avançada de palavras"""
        filtered = []
        
        for word in words:
            # Remove stop words
            if word in self._stop_words:
                continue
            
            # Remove palavras muito curtas
            if len(word) < 3:
                continue
            
            # Remove palavras que são apenas repetições
            if len(set(word)) == 1:
                continue
            
            # Remove palavras que parecem códigos/IDs
            if re.match(r'^[a-z]{1,2}\d+$', word):
                continue
            
            filtered.append(word)
        
        return filtered
    
    def _simple_stem(self, words: List[str]) -> List[str]:
        """Stemming simples baseado em regras"""
        stemmed = []
        
        for word in words:
            # Aplica regras de stemming
            for suffix, replacement in self._suffix_rules:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    word = word[:-len(suffix)] + replacement
                    break
            
            stemmed.append(word)
        
        return stemmed
