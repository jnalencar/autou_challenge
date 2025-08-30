# 🔒 GUIA DE SEGURANÇA - EMAIL PROCESSOR API

## 🛡️ Medidas de Segurança Implementadas

### ✅ 1. Proteção de Credenciais
- **Arquivo .env**: API keys e secrets nunca ficam no código
- **Validação**: Sistema alerta se using chaves padrão inseguras
- **Gitignore**: Previne commit acidental de credenciais

### ✅ 2. Validação de Arquivos
- **Tamanho**: Limite de 10MB por arquivo
- **Tipos**: Apenas .pdf, .eml, .txt permitidos
- **Assinatura**: Verifica se o arquivo é realmente do tipo declarado
- **Conteúdo**: Sanitização básica contra arquivos maliciosos

### ✅ 3. Headers de Segurança
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'
```

### ✅ 4. CORS Configurável
- **Desenvolvimento**: Permite localhost
- **Produção**: Configure apenas origens confiáveis

### ✅ 5. Rate Limiting (Opcional)
- **60 requisições por minuto** por IP
- Previne ataques de força bruta

### ✅ 6. Tratamento de Erros
- **Produção**: Não expõe detalhes internos
- **Desenvolvimento**: Logs detalhados para debug

### ✅ 7. Documentação Restrita
- **Swagger/ReDoc**: Disponível apenas em desenvolvimento
- **Produção**: Endpoints de debug desabilitados

## 🚨 Configurações Críticas de Segurança

### 1. Configure o arquivo .env
```bash
# Copie o exemplo
cp .env.example .env

# Edite com suas credenciais
nano .env
```

### 2. Gere chaves seguras
```bash
# Para SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Para JWT_SECRET_KEY  
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Configure CORS para produção
```env
# NÃO use * em produção!
CORS_ORIGINS=https://seudominio.com,https://app.seudominio.com
```

### 4. Configurações de produção
```env
DEBUG=False
API_RELOAD=False
```

## 🔧 Configurações Recomendadas por Ambiente

### 🏠 Desenvolvimento
```env
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500
API_RELOAD=True
```

### 🏭 Produção
```env
DEBUG=False
CORS_ORIGINS=https://seudominio.com
API_RELOAD=False
SECRET_KEY=sua_chave_super_segura_aqui
```

## 🛡️ Sugestões Adicionais de Segurança

### 1. **HTTPS Obrigatório**
```bash
# Use um proxy reverso (nginx/apache)
# Redirecione HTTP → HTTPS
# Configure certificados SSL
```

### 2. **Firewall e Rede**
```bash
# Exponha apenas as portas necessárias
# Use VPN para acesso interno
# Configure rate limiting no nginx
```

### 3. **Monitoramento**
```python
# Implemente logs de auditoria
# Monitore tentativas de ataque
# Configure alertas para falhas
```

### 4. **Backup e Recuperação**
```bash
# Backup automático de configurações
# Plano de recuperação de desastres
# Teste regularmente os backups
```

### 5. **Autenticação (Futuro)**
```python
# JWT tokens para APIs privadas
# API keys para clientes
# OAuth2 para integração
```

## 🚨 Checklist de Segurança

### Antes de usar em produção:
- [ ] Configurar .env com chaves reais
- [ ] Configurar CORS restritivo
- [ ] Desabilitar DEBUG
- [ ] Configurar HTTPS
- [ ] Testar validação de arquivos
- [ ] Configurar logs de segurança
- [ ] Implementar monitoramento
- [ ] Documentar procedimentos de emergência

### Manutenção regular:
- [ ] Atualizar dependências
- [ ] Revisar logs de segurança
- [ ] Testar backups
- [ ] Auditar acessos
- [ ] Rotacionar chaves secretas

## 🆘 Em Caso de Incidente

1. **Isole** o sistema afetado
2. **Identifique** o vetor de ataque
3. **Colete** evidências nos logs
4. **Mitigue** a vulnerabilidade
5. **Restaure** de backup se necessário
6. **Documente** o incidente
7. **Melhore** as defesas

## 📞 Contatos de Emergência

```
Administrador: [seu-email]
Equipe de TI: [ti-email]
Logs: /var/log/emailprocessor/
Backup: /backup/emailprocessor/
```

---

**⚠️ IMPORTANTE**: Esta API processa conteúdo sensível (emails). Siga todas as práticas de segurança e regulamentações aplicáveis (LGPD, GDPR, etc.).
