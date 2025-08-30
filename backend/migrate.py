"""
Script de migração do código antigo para a nova arquitetura Clean Code
"""

import os
import shutil
from pathlib import Path

def migrate_to_clean_architecture():
    """Migra do main.py antigo para a nova estrutura"""
    
    backend_path = Path(".")
    
    # 1. Faz backup do main.py original
    if (backend_path / "main.py").exists():
        shutil.copy2("main.py", "main_legacy.py")
        print("✅ Backup do main.py criado como main_legacy.py")
    
    # 2. Substitui o main.py pelo novo
    if (backend_path / "main_clean.py").exists():
        shutil.copy2("main_clean.py", "main.py")
        print("✅ main.py atualizado com a nova arquitetura")
    
    # 3. Verifica se a estrutura src/ existe
    if (backend_path / "src").exists():
        print("✅ Nova estrutura de diretórios criada")
    else:
        print("❌ Estrutura src/ não encontrada")
        return False
    
    # 4. Lista os benefícios da migração
    print("\n🎉 Migração concluída com sucesso!")
    print("\n📋 Benefícios da nova arquitetura:")
    print("   • Código mais limpo e organizado")
    print("   • Separação clara de responsabilidades") 
    print("   • Fácil manutenção e extensão")
    print("   • Testabilidade melhorada")
    print("   • Princípios SOLID aplicados")
    print("   • Clean Architecture implementada")
    
    print("\n🚀 Para executar:")
    print("   python main.py")
    
    print("\n📁 Nova estrutura:")
    print("   src/domain/      - Entidades e regras de negócio")
    print("   src/application/ - Casos de uso")
    print("   src/infrastructure/ - Implementações concretas")
    print("   src/presentation/ - Controllers e modelos")
    
    return True

if __name__ == "__main__":
    migrate_to_clean_architecture()
