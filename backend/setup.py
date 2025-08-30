#!/usr/bin/env python3
"""
Script de setup para configuração inicial segura do Email Processor API
"""

import os
import secrets
import shutil
from pathlib import Path

def generate_secure_key():
    """Gera uma chave segura"""
    return secrets.token_urlsafe(32)

def setup_security():
    """Configura aspectos de segurança básicos"""
    print("🔒 Configurando segurança...")
    
    # 1. Verifica se .env existe
    if not Path(".env").exists():
        if Path(".env.example").exists():
            shutil.copy2(".env.example", ".env")
            print("✅ Arquivo .env criado a partir do exemplo")
        else:
            print("❌ Arquivo .env.example não encontrado")
            return False
    
    # 2. Gera chaves seguras
    secret_key = generate_secure_key()
    jwt_key = generate_secure_key()
    
    print(f"\n🔑 Chaves geradas:")
    print(f"SECRET_KEY={secret_key}")
    print(f"JWT_SECRET_KEY={jwt_key}")
    
    # 3. Atualiza .env
    env_content = Path(".env").read_text()
    
    # Substitui chaves inseguras
    env_content = env_content.replace(
        "SECRET_KEY=seu_secret_key_super_seguro_aqui_mude_isso",
        f"SECRET_KEY={secret_key}"
    )
    env_content = env_content.replace(
        "JWT_SECRET_KEY=outro_secret_key_para_jwt_mude_isso_tambem",
        f"JWT_SECRET_KEY={jwt_key}"
    )
    
    Path(".env").write_text(env_content)
    print("✅ Chaves atualizadas no arquivo .env")
    
    return True

def check_requirements():
    """Verifica se as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    try:
        import fastapi
        import uvicorn
        import dotenv
        print("✅ Dependências principais encontradas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def validate_gemini_key():
    """Valida se a API key do Gemini está configurada"""
    print("🤖 Verificando configuração do Gemini...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "sua_api_key_do_gemini_aqui":
        print("❌ API Key do Gemini não configurada")
        print("Configure GEMINI_API_KEY no arquivo .env")
        print("Obtenha em: https://aistudio.google.com/")
        return False
    
    print("✅ API Key do Gemini configurada")
    return True

def main():
    """Função principal do setup"""
    print("🚀 Setup do Email Processor API")
    print("=" * 40)
    
    success = True
    
    # 1. Verifica dependências
    if not check_requirements():
        success = False
    
    # 2. Configura segurança
    if not setup_security():
        success = False
    
    # 3. Valida Gemini
    if not validate_gemini_key():
        success = False
    
    print("\n" + "=" * 40)
    
    if success:
        print("🎉 Setup concluído com sucesso!")
        print("\n🚀 Para iniciar a aplicação:")
        print("   python main_secure.py")
        print("\n📖 Para mais informações:")
        print("   Leia SECURITY.md")
    else:
        print("❌ Setup incompleto!")
        print("Corrija os problemas acima antes de continuar.")
    
    print("\n⚠️  IMPORTANTE:")
    print("- NUNCA commite o arquivo .env")
    print("- Configure CORS adequadamente para produção")
    print("- Use HTTPS em produção")

if __name__ == "__main__":
    main()
