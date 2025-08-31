from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import nltk
import re
import json
import io
from unidecode import unidecode
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from PyPDF2 import PdfReader
import dotenv
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Baixar os recursos necessários do NLTK
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    nltk.download('rslp')

# Inicializar o stemmer para português
stemmer = RSLPStemmer()

def extract_text_from_pdf(file_content):
    """
    Extrai texto de um arquivo PDF
    """
    try:
        pdf_reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        text = text.strip()
        
        if len(text) < 10:
            return f"PDF processado mas pouco texto encontrado: '{text[:50]}...'"
        
        return text
    except Exception as e:
        return f"Erro ao extrair texto do PDF: {str(e)}"

def extract_text_from_eml(file_content):
    """
    Extrai texto de um arquivo EML (email)
    """
    try:
        # Primeiro, tenta uma abordagem simples com regex
        if isinstance(file_content, bytes):
            content_str = file_content.decode('utf-8', errors='ignore')
        else:
            content_str = str(file_content)
        
        # Extrai subject
        subject_match = re.search(r'Subject:\s*([^\r\n]+)', content_str, re.IGNORECASE)
        subject = subject_match.group(1).strip() if subject_match else 'Sem assunto'
        
        # Extrai from
        from_match = re.search(r'From:\s*([^\r\n]+)', content_str, re.IGNORECASE)
        from_addr = from_match.group(1).strip() if from_match else 'Remetente desconhecido'
        
        # Procura pelo conteúdo text/plain primeiro
        plain_text_pattern = r'Content-Type:\s*text/plain.*?\n\n(.*?)(?=--\w+|$)'
        plain_match = re.search(plain_text_pattern, content_str, re.DOTALL | re.IGNORECASE)
        
        if plain_match:
            body = plain_match.group(1).strip()
        else:
            # Se não encontrar text/plain, procura por text/html
            html_pattern = r'Content-Type:\s*text/html.*?\n\n(.*?)(?=--\w+|$)'
            html_match = re.search(html_pattern, content_str, re.DOTALL | re.IGNORECASE)
            
            if html_match:
                html_body = html_match.group(1).strip()
                # Remove tags HTML
                body = re.sub(r'<[^>]+>', '', html_body)
                body = re.sub(r'&nbsp;', ' ', body)
                body = re.sub(r'&[a-zA-Z0-9]+;', '', body)
            else:
                # Fallback: pega tudo após os headers
                header_end = content_str.find('\n\n')
                if header_end != -1:
                    body = content_str[header_end + 2:].strip()
                    # Remove boundaries
                    body = re.sub(r'--\w+.*', '', body, flags=re.DOTALL)
                else:
                    body = "Não foi possível extrair o corpo do email" 
        
        # Limpa quoted-printable encoding
        body = re.sub(r'=\r?\n', '', body)  # Remove line breaks
        body = re.sub(r'=([0-9A-F]{2})', lambda m: chr(int(m.group(1), 16)), body)
        
        # Limpa espaços extras
        body = re.sub(r'\n\s*\n', '\n\n', body)
        body = body.strip()
        
        if not body or len(body.strip()) < 10:
            # Se ainda não conseguiu extrair, tenta uma abordagem mais agressiva
            lines = content_str.split('\n')
            content_started = False
            extracted_lines = []
            
            for line in lines:
                if content_started:
                    if line.startswith('--') and 'boundary' in content_str:
                        break
                    if not line.startswith('Content-'):
                        extracted_lines.append(line)
                elif line.strip() == '' and not content_started:
                    content_started = True
            
            body = '\n'.join(extracted_lines).strip()
        
        full_text = f"Assunto: {subject}\nDe: {from_addr}\n\n{body}"
        return full_text
        
    except Exception as e:
        # Fallback simples - pega tudo que parecer ser texto
        try:
            if isinstance(file_content, bytes):
                content_str = file_content.decode('utf-8', errors='ignore')
            else:
                content_str = str(file_content)
            
            # Remove tudo que claramente não é conteúdo
            content_str = re.sub(r'MIME-Version:.*?\n', '', content_str)
            content_str = re.sub(r'Content-Type:.*?\n', '', content_str)
            content_str = re.sub(r'Content-Transfer-Encoding:.*?\n', '', content_str)
            content_str = re.sub(r'--\w+.*?\n', '', content_str)
            
            return f"Email extraído (método simplificado):\n{content_str.strip()}"
            
        except Exception as fallback_error:
            return f"Conteúdo do arquivo EML (erro na extração: {str(e)})"

def extract_text_from_file(file: UploadFile):
    """
    Extrai texto de diferentes tipos de arquivo
    """
    try:
        file_content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        filename = file.filename.lower() if file.filename else ""
        
        if filename.endswith('.pdf'):
            return extract_text_from_pdf(file_content)
        elif filename.endswith('.eml'):
            return extract_text_from_eml(file_content)
        elif filename.endswith(('.txt', '.text')):
            # Para arquivos de texto
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                return file_content.decode('latin-1', errors='ignore')
        else:
            # Para outros tipos, tenta decodificar como texto
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return file_content.decode('latin-1', errors='ignore')
                except Exception as e:
                    return f"Erro: Tipo de arquivo não suportado ou corrompido. Arquivo: {file.filename}, Erro: {str(e)}"
    except Exception as e:
        return f"Erro ao processar arquivo {file.filename}: {str(e)}"

def preprocess_text(text):
    """
    Função para pré-processamento de texto:
    - Remove acentos
    - Converte para minúsculas
    - Remove pontuação
    - Remove números
    - Remove stop words
    - Aplica stemming
    """
    # Remove acentos
    text = unidecode(text)
    
    # Converte para minúsculas
    text = text.lower()
    
    # Remove pontuação e números
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    
    # Tokeniza o texto
    words = nltk.word_tokenize(text, language='portuguese')
    
    # Remove stop words em português
    stop_words = set(stopwords.words('portuguese'))
    words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Aplica stemming
    words = [stemmer.stem(word) for word in words]
    
    # Reconstrói o texto
    processed_text = ' '.join(words)
    
    return processed_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou especifique ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/processar")
async def process_email(body: str = Form(""), subject: str = Form(""), file: UploadFile = File(None)):
    try:
        # Determina o conteúdo a ser processado
        content = ""
        
        if file:
            # Se um arquivo foi enviado, extrai o texto dele
            extracted_content = extract_text_from_file(file)
            if extracted_content and len(extracted_content.strip()) >= 10:
                content = extracted_content
        
        # Se não há conteúdo do arquivo, usa o texto do body
        if not content and body and len(body.strip()) >= 10:
            content = body
            
        # Adiciona o subject se fornecido
        if subject and subject.strip():
            if content:
                content = f"Assunto: {subject.strip()}\n\n{content}"
            else:
                content = f"Assunto: {subject.strip()}"
        
        # Verifica se há conteúdo válido
        if not content or len(content.strip()) < 10:
            return {
                "categoria": "Erro",
                "resposta": "Nenhum conteúdo fornecido. Envie um texto ou arquivo com conteúdo válido.",
                "erro": "Conteúdo insuficiente"
            }
        
        # Pré-processa o texto para reduzir tokens
        processed_body = preprocess_text(content)
        
        # Uma única consulta que classifica e gera resposta adequada para cada categoria
        prompt = f"""
        Analise o seguinte email e execute as seguintes tarefas:

        1. Classifique como 'Produtivo' ou 'Improdutivo'
        2. Gere uma resposta automática adequada à categoria:
           - Se PRODUTIVO: resposta que facilita o diálogo e encoraja comunicação
           - Se IMPRODUTIVO: resposta educada mas que desencoraja continuidade

        Email (pré-processado): {processed_body}
        Email original (para contexto): {content}

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
        
        response = model.generate_content(prompt)
        
        try:
            # Remove markdown code blocks se existirem
            response_text = response.text.strip()
            
            # Remove ```json e ``` se existirem
            if response_text.startswith('```json'):
                response_text = response_text[7:]  # Remove ```json
            elif response_text.startswith('```'):
                response_text = response_text[3:]   # Remove ```
                
            if response_text.endswith('```'):
                response_text = response_text[:-3]  # Remove ``` do final
                
            response_text = response_text.strip()
            
            # Tenta fazer parse do JSON limpo
            result = json.loads(response_text)
            
            return result
        except json.JSONDecodeError as e:
            # Se falhar no parse JSON, retorna resposta com texto bruto
            return {
                "categoria": "Erro",
                "resposta": "Desculpe, ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde.",
                "erro_json": str(e),
                "resposta_bruta": response.text
            }
    except Exception as e:
        # Captura qualquer outro erro
        return {
            "categoria": "Erro",
            "resposta": "Desculpe, ocorreu um erro interno. Tente novamente mais tarde.",
            "erro": str(e),
            "tipo_erro": type(e).__name__
        }

@app.post("/debug-eml")
async def debug_eml_file(file: UploadFile = File(...)):
    """
    Endpoint para debug específico de arquivos EML
    """
    try:
        file_content = file.file.read()
        file.file.seek(0)
        
        # Informações básicas do arquivo
        info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(file_content),
            "first_100_chars": file_content[:100].decode('utf-8', errors='ignore')
        }
        
        # Tenta extrair o texto
        extracted_text = extract_text_from_eml(file_content)
        
        return {
            "file_info": info,
            "extracted_text": extracted_text,
            "extraction_success": not extracted_text.startswith("Erro"),
            "status": "success"
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "filename": file.filename,
            "status": "error"
        }

@app.post("/extract-text")
async def extract_text_endpoint(file: UploadFile = File(...)):
    """
    Endpoint para testar extração de texto de arquivos
    """
    try:
        extracted_text = extract_text_from_file(file)
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "extracted_text": extracted_text,
            "text_length": len(extracted_text),
            "extraction_success": not ("Erro" in extracted_text and extracted_text.startswith("Erro")),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "filename": file.filename,
            "status": "error"
        }

@app.post("/preprocess")
async def test_preprocessing(body: str = Form(...)):
    """
    Endpoint para testar apenas o pré-processamento do texto
    """
    try:
        processed_body = preprocess_text(body)
        return {
            "original": body,
            "processed": processed_body,
            "token_reduction": f"{len(body.split())} -> {len(processed_body.split())} palavras",
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }

@app.post("/test")
async def test_simple():
    """
    Endpoint de teste simples
    """
    return {"message": "API funcionando!", "status": "ok"}
