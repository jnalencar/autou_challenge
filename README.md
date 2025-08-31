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
│   ├── parsers/         # Parsers de arquivo
│   └── security/        # Middlewares de segurança
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
- **Segurança Robusta**: Headers de segurança, validação de arquivos, rate limiting

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Git
- API Key do Google Gemini ([obtenha aqui](https://aistudio.google.com/))

### Passo 1: Clone o Repositório
```bash
git clone https://github.com/jnalencar/autou_challenge.git
cd autou_challenge
```

### Passo 2: Configure o Backend
```bash
# Entre no diretório do backend
cd backend

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Passo 3: Configure Segurança (OBRIGATÓRIO)
```bash
# Execute o script de setup automático
python setup.py
```

**OU configure manualmente:**

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e configure:
# - GEMINI_API_KEY (obrigatório)
# - SECRET_KEY (será gerado automaticamente)
# - JWT_SECRET_KEY (será gerado automaticamente)
```

### Passo 4: Execute a Aplicação

**Opção 1 - Versão Segura (Recomendada):**
```bash
python main_secure.py
```

**Opção 2 - Versão Limpa (Clean Architecture):**
```bash
python main_clean.py
```

**Opção 3 - Versão Original (Backup):**
```bash
python main_legacy.py
```

### Passo 5: Configure o Frontend
```bash
# Em outro terminal, vá para o frontend
cd ../frontend

# Abra o arquivo index.html em um servidor local
# Opção 1 - Python:
python -m http.server 5500

# Opção 2 - Node.js (se tiver instalado):
npx serve .

# Opção 3 - VS Code Live Server
# Clique direito no index.html > "Open with Live Server"
```

### Passo 6: Acesse a Aplicação
- **Backend API**: http://127.0.0.1:8000
- **Frontend**: http://127.0.0.1:5500
- **Documentação API**: http://127.0.0.1:8000/docs (apenas em desenvolvimento)

## 🔒 Configuração de Segurança

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

## 📡 Endpoints da API

### Endpoints Principais:
- `POST /processar` - Processa e analisa emails
- `POST /extract-text` - Extrai texto de arquivos
- `POST /preprocess` - Testa pré-processamento
- `GET /health` - Health check

### Endpoints de Debug (apenas desenvolvimento):
- `POST /debug-eml` - Debug específico para arquivos EML
- `POST /test` - Teste simples da API

## 💻 Uso da Interface Web

1. **Abra o frontend** no navegador
2. **Digite um email** na caixa de texto OU **arraste um arquivo** (.pdf, .eml, .txt)
3. **Adicione um assunto** (opcional)
4. **Clique em "Processar"**
5. **Veja o resultado** com categoria e resposta gerada

## 🧪 Testando a API

### Usando curl:
```bash
# Teste simples
curl -X POST "http://127.0.0.1:8000/processar" \
  -F "body=Olá, preciso de ajuda com meu pedido" \
  -F "subject=Solicitação de suporte"

# Upload de arquivo
curl -X POST "http://127.0.0.1:8000/processar" \
  -F "file=@email.eml" \
  -F "subject=Email importado"
```

### Usando a documentação interativa:
Acesse http://127.0.0.1:8000/docs para testar os endpoints diretamente no navegador.

## 🔧 Configuração para Produção

### 1. Configure variáveis de ambiente:
```env
DEBUG=False
API_RELOAD=False
CORS_ORIGINS=https://seudominio.com
SECRET_KEY=sua_chave_super_segura
```

### 2. Use HTTPS:
```bash
# Com nginx/apache como proxy reverso
# Configure certificados SSL
# Force redirecionamento HTTP → HTTPS
```

### 3. Configure monitoramento:
- Logs centralizados
- Alertas de segurança
- Métricas de performance

## 🆘 Solução de Problemas

### Problema: "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### Problema: "GEMINI_API_KEY não configurada"
1. Obtenha uma API key em https://aistudio.google.com/
2. Configure no arquivo .env: `GEMINI_API_KEY=sua_key_aqui`

### Problema: "CORS Error"
1. Verifique se o backend está rodando
2. Configure CORS_ORIGINS no .env para incluir seu frontend

### Problema: "Rate limit excedido"
- Aguarde 1 minuto ou configure RATE_LIMIT_CALLS no .env

## 📋 Scripts Disponíveis

- `python setup.py` - Configuração inicial automática
- `python migrate.py` - Migração de arquitetura (já executado)
- `python main_secure.py` - Executa versão segura
- `python main_clean.py` - Executa versão com Clean Architecture
- `python main_legacy.py` - Executa versão original

## 📚 Documentação Adicional

- **SECURITY.md** - Guia completo de segurança
- **SECURITY_IMPLEMENTATION.md** - Detalhes das implementações
- **REFACTORING_SUMMARY.md** - Resumo da refatoração

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

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte a documentação em `SECURITY.md`
2. Verifique os logs de erro
3. Execute `python setup.py` para reconfigurar
4. Crie uma issue no repositório
