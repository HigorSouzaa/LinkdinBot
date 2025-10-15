# -*- coding: utf-8 -*-
"""
Script de teste para verificar se o bot está funcionando
"""

import sys
import os

# Forçar UTF-8
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

print("=" * 60)
print("🧪 TESTE DO LINKEDIN BOT")
print("=" * 60)

# Teste 1: Importar módulos
print("\n1️⃣ Testando importação de módulos...")
try:
    import config
    import constants
    import utils
    from linkedin import LinkedinBot
    print("✅ Todos os módulos importados com sucesso!")
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    sys.exit(1)

# Teste 2: Verificar métodos da classe
print("\n2️⃣ Testando métodos da classe LinkedinBot...")
required_methods = ['startApplying', 'easyApply', 'finish', 'generateUrls', 'start']
missing_methods = []

for method in required_methods:
    if not hasattr(LinkedinBot, method):
        missing_methods.append(method)
        print(f"❌ Método '{method}' não encontrado!")
    else:
        print(f"✅ Método '{method}' OK")

if missing_methods:
    print(f"\n❌ Métodos faltando: {missing_methods}")
    sys.exit(1)

# Teste 3: Verificar config
print("\n3️⃣ Testando configurações...")
try:
    assert hasattr(config, 'location'), "location não encontrado"
    assert hasattr(config, 'keywords'), "keywords não encontrado"
    assert hasattr(config, 'botSpeed'), "botSpeed não encontrado"
    assert hasattr(config, 'maxApplications'), "maxApplications não encontrado"
    
    print(f"✅ Localizações: {config.location}")
    print(f"✅ Palavras-chave: {config.keywords}")
    print(f"✅ Velocidade: {config.botSpeed}s")
    print(f"✅ Limite: {config.maxApplications}")
except AssertionError as e:
    print(f"❌ Configuração inválida: {e}")
    sys.exit(1)

# Teste 4: Verificar pasta selenium_profile
print("\n4️⃣ Testando sistema de perfil...")
if os.path.exists("selenium_profile"):
    print("✅ Pasta selenium_profile existe (login salvo)")
else:
    print("⚠️ Pasta selenium_profile não existe (primeira execução)")
    print("   → Você precisará fazer login no LinkedIn na primeira vez")

# Teste 5: Verificar encoding
print("\n5️⃣ Testando encoding UTF-8...")
try:
    test_chars = "✅ ❌ ⚠️ 🚀 📊 🎯"
    print(f"Emojis: {test_chars}")
    print("✅ Encoding UTF-8 funcionando!")
except Exception as e:
    print(f"⚠️ Problema com encoding: {e}")

print("\n" + "=" * 60)
print("✅ TODOS OS TESTES PASSARAM!")
print("=" * 60)
print("\n🚀 O bot está pronto para usar!")
print("\nPara executar:")
print("  • Interface gráfica: python gui_config.py")
print("  • Linha de comando: python linkedin.py")
print("\n⚠️ LEMBRE-SE: Na primeira execução, faça login no LinkedIn")
