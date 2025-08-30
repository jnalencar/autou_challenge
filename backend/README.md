# Email Processor API

API moderna para processamento e análise de emails usando IA, desenvolvida com Clean Architecture, SOLID e Clean Code.

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture** com as seguintes camadas:

```
src/
├── domain/              # Camada de Domínio (Entidades + Interfaces)
│   ├── entities/        # Entidades de negócio
│   └── services/        # Interfaces dos serviços
├── application/         # Camada de Aplicação (Casos de Uso)
│   └── use_cases/       # Casos de uso da aplicação
├── infrastructure/     # Camada de Infraestrutura
│   ├── external/        # Serviços externos (IA, NLTK)
│   └── parsers/         # Parsers de arquivo
└── presentation/       # Camada de Apresentação
    ├── controllers/     # Controllers FastAPI
    └── models/          # Modelos de request/response
```

## 🚀 Funcionalidades

- **Análise de Emails**: Classifica emails como "Produtivo" ou "Improdutivo"
- **Respostas Automáticas**: Gera respostas adequadas para cada categoria
- **Suporte a Arquivos**: PDF, EML, TXT
- **Pré-processamento**: Remove stop words, aplica stemming
- **IA Integrada**: Usa Google Gemini para análise

## 📦 Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. **Configure segurança** (OBRIGATÓRIO):
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Configure suas credenciais
# NUNCA use as chaves padrão em produção!
nano .env
```

4. Execute a aplicação:
```bash
# Versão segura (recomendada)
python main_secure.py

# Ou versão original
python main_legacy.py
```

## � Configuração de Segurança

### Chaves Obrigatórias (.env):
```env
GEMINI_API_KEY=sua_api_key_aqui
SECRET_KEY=gere_uma_chave_segura
JWT_SECRET_KEY=gere_outra_chave_segura
```

### Gerar chaves seguras:
```bash
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

## 🛡️ Recursos de Segurança

- **🔐 Proteção de Credenciais**: API keys em .env
- **📁 Validação de Arquivos**: Tipo, tamanho e assinatura
- **🌐 Headers de Segurança**: Proteção contra XSS, clickjacking
- **🚦 Rate Limiting**: Prevenção de ataques DDoS
- **🎯 CORS Configurável**: Controle de acesso por origem
- **🔍 Logs de Segurança**: Monitoramento de atividades

## 📡 Endpoints

- `POST /processar` - Processa e analisa emails
- `POST /extract-text` - Extrai texto de arquivos
- `POST /preprocess` - Testa pré-processamento
- `GET /health` - Health check

## 🏛️ Princípios Aplicados

### Clean Code
- Nomes descritivos e significativos
- Funções pequenas e focadas
- Código auto-documentado
- Tratamento de erros consistente

### SOLID
- **S**ingle Responsibility: Cada classe tem uma única responsabilidade
- **O**pen/Closed: Extensível sem modificação (Factory Pattern)
- **L**iskov Substitution: Interfaces bem definidas
- **I**nterface Segregation: Interfaces específicas
- **D**ependency Inversion: Depende de abstrações

### Clean Architecture
- Separação clara de responsabilidades
- Dependências apontam para dentro
- Camadas bem definidas
- Testabilidade alta
