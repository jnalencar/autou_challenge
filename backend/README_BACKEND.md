# Email Processor API - Backend

Este é o backend da aplicação Email Processor API, desenvolvido com Clean Architecture, SOLID e Clean Code.

## 🚀 Início Rápido

```bash
# Instale dependências
pip install -r requirements.txt

# Configure segurança automaticamente
python setup.py

# Execute a aplicação
python main.py
```

## 📁 Estrutura do Backend

```
backend/
├── src/                    # Código fonte (Clean Architecture)
│   ├── domain/            # Regras de negócio
│   ├── application/       # Casos de uso
│   ├── infrastructure/    # Implementações
│   └── presentation/      # Controllers e modelos
├── main.py               # Aplicação principal
├── config.py              # Configurações
├── .env                   # Variáveis de ambiente (configure!)
└── requirements.txt       # Dependências
```

## 🔒 Configuração Obrigatória

1. **Configure API Key do Gemini**:
   - Obtenha em: https://aistudio.google.com/
   - Configure no arquivo `.env`

2. **Execute setup automático**:
   ```bash
   python setup.py
   ```

## 🏗️ Arquitetura Implementada

### Princípios SOLID ✅
- **S**ingle Responsibility: Cada classe tem uma função
- **O**pen/Closed: Extensível sem modificação
- **L**iskov Substitution: Interfaces bem definidas
- **I**nterface Segregation: Contratos específicos
- **D**ependency Inversion: Depende de abstrações

### Clean Architecture ✅
- **Domain**: Entidades e regras de negócio
- **Application**: Casos de uso
- **Infrastructure**: Implementações concretas
- **Presentation**: Interface (controllers)

### Segurança ✅
- Variáveis de ambiente (.env)
- Headers de segurança
- Validação de arquivos
- Rate limiting
- Tratamento de exceções

## 📡 Endpoints Disponíveis

- `POST /processar` - Processa emails
- `POST /extract-text` - Extrai texto de arquivos
- `POST /preprocess` - Pré-processamento
- `GET /health` - Health check
- `GET /docs` - Documentação (desenvolvimento)

## 🧪 Testando

### Via Interface Web:
1. Execute o frontend: `cd ../frontend && python -m http.server 5500`
2. Acesse: http://127.0.0.1:5500

### Via API direta:
```bash
curl -X POST "http://127.0.0.1:8000/processar" \
  -F "body=Teste de email" \
  -F "subject=Assunto do teste"
```

### Via Documentação:
Acesse: http://127.0.0.1:8000/docs

## 📚 Documentação Completa

- **[README Principal](../README.md)** - Tutorial completo
- **[QUICKSTART](../QUICKSTART.md)** - Início em 5 minutos
- **[SECURITY.md](SECURITY.md)** - Guia de segurança
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Resumo da refatoração

## 🆘 Solução de Problemas

### Erro de configuração:
```bash
python setup.py  # Reconfigure automaticamente
```

### Dependências faltando:
```bash
pip install -r requirements.txt
```

### API Key não configurada:
1. Edite `.env`
2. Configure `GEMINI_API_KEY=sua_key`

---

Para tutorial completo, consulte o **[README principal](../README.md)**.
