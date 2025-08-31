# 🚀 INÍCIO RÁPIDO - Email Processor API

## ⚡ Execução em 5 Minutos

### 1. Clone e Configure
```bash
# Clone o repositório
git clone https://github.com/jnalencar/autou_challenge.git
cd autou_challenge/backend

# Instale dependências
pip install -r requirements.txt

# Configure automaticamente (OBRIGATÓRIO)
python setup.py
```

### 2. Configure API Key do Gemini
1. Acesse https://aistudio.google.com/
2. Crie uma API key gratuita
3. Edite o arquivo `.env` e coloque sua key:
```env
GEMINI_API_KEY=sua_api_key_aqui
```

### 3. Execute
```bash
# Execute o backend
python main.py
```

### 4. Abra o Frontend
```bash
# Em outro terminal
cd ../frontend
python -m http.server 5500
```

### 5. Teste
- Abra http://127.0.0.1:5500 no navegador
- Digite um email ou arraste um arquivo
- Clique em "Processar"
- Veja a análise da IA!

## 🎯 URLs Importantes

- **Frontend**: http://127.0.0.1:5500
- **Backend API**: http://127.0.0.1:8000
- **Documentação**: http://127.0.0.1:8000/docs

## 💡 Dicas

- Use `python setup.py` se houver erro de configuração
- Consulte `README.md` para tutorial completo
- Veja `SECURITY.md` para configurações avançadas

## 🆘 Problemas Comuns

### "No module named 'dotenv'"
```bash
pip install python-dotenv
```

### "GEMINI_API_KEY não configurada"
```bash
# Edite o arquivo .env e adicione sua API key
```

### "CORS Error"
```bash
# Certifique-se que backend está rodando na porta 8000
```

---

**Pronto! Sua API está funcionando! 🎉**
