# -*- coding: utf-8 -*-
"""
Script de teste para verificar seletores do LinkedIn
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

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import utils

print("="*60)
print("🔍 TESTE DE SELETORES DO LINKEDIN")
print("="*60)

# Inicializar Chrome
print("\n1️⃣ Inicializando Chrome...")
options = utils.chromeBrowserOptions()
driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

try:
    # URL de teste
    test_url = "https://www.linkedin.com/jobs/search/?keywords=python&location=Brazil&f_AL=true"
    
    print(f"\n2️⃣ Acessando: {test_url[:80]}...")
    driver.get(test_url)
    
    print("\n⏳ Aguardando 10 segundos para carregar...")
    time.sleep(10)
    
    print("\n3️⃣ Testando seletores CSS:")
    
    selectors = [
        ".jobs-search-results__list-item",
        ".jobs-search__results-list li",
        "li[data-occludable-job-id]",
        ".scaffold-layout__list-container li",
        "ul.jobs-search__results-list > li",
        ".job-card-container",
        ".jobs-search-results-list__list-item"
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if len(elements) > 0:
                print(f"✅ '{selector}' → {len(elements)} elementos")
            else:
                print(f"⚠️ '{selector}' → 0 elementos")
        except Exception as e:
            print(f"❌ '{selector}' → Erro: {str(e)[:50]}")
    
    print("\n4️⃣ Testando XPath:")
    xpaths = [
        "//li[contains(@class, 'jobs')]",
        "//li[@data-occludable-job-id]",
        "//div[contains(@class, 'job-card')]"
    ]
    
    for xpath in xpaths:
        try:
            elements = driver.find_elements(By.XPATH, xpath)
            if len(elements) > 0:
                print(f"✅ '{xpath}' → {len(elements)} elementos")
            else:
                print(f"⚠️ '{xpath}' → 0 elementos")
        except Exception as e:
            print(f"❌ '{xpath}' → Erro: {str(e)[:50]}")
    
    print("\n5️⃣ Salvando HTML da página...")
    with open("linkedin_test_page.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("✅ Salvo em: linkedin_test_page.html")
    
    print("\n6️⃣ Analisando classes na página...")
    all_classes = set()
    all_elements = driver.find_elements(By.XPATH, "//*[@class]")
    for elem in all_elements[:100]:  # Primeiros 100 elementos
        classes = elem.get_attribute("class").split()
        all_classes.update(classes)
    
    job_related_classes = [c for c in all_classes if 'job' in c.lower()]
    print(f"\nClasses relacionadas a 'job' encontradas:")
    for cls in sorted(job_related_classes)[:20]:
        print(f"  • {cls}")
    
    print("\n" + "="*60)
    print("✅ TESTE CONCLUÍDO!")
    print("="*60)
    print("\n📋 Próximos passos:")
    print("1. Verifique linkedin_test_page.html")
    print("2. Procure por elementos com classe 'job'")
    print("3. Atualize os seletores no código se necessário")
    
    input("\n⏸️ Pressione ENTER para fechar o navegador...")

finally:
    driver.quit()
    print("\n✅ Navegador fechado")
