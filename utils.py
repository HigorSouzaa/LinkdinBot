# -*- coding: utf-8 -*-
"""
Utils - Funções auxiliares para o LinkedIn Bot
"""

import sys
import os

# Forçar encoding UTF-8 no Windows
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul 2>&1")
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def prRed(text):
    """Imprime texto em vermelho"""
    try:
        print(f"\033[91m{text}\033[00m", flush=True)
    except (UnicodeEncodeError, UnicodeDecodeError):
        clean_text = str(text).encode('ascii', 'ignore').decode('ascii')
        print(f"\033[91m{clean_text}\033[00m", flush=True)


def prGreen(text):
    """Imprime texto em verde"""
    try:
        print(f"\033[92m{text}\033[00m", flush=True)
    except (UnicodeEncodeError, UnicodeDecodeError):
        clean_text = str(text).encode('ascii', 'ignore').decode('ascii')
        print(f"\033[92m{clean_text}\033[00m", flush=True)


def prYellow(text):
    """Imprime texto em amarelo"""
    try:
        print(f"\033[93m{text}\033[00m", flush=True)
    except (UnicodeEncodeError, UnicodeDecodeError):
        clean_text = str(text).encode('ascii', 'ignore').decode('ascii')
        print(f"\033[93m{clean_text}\033[00m", flush=True)


def prBlue(text):
    """Imprime texto em azul"""
    try:
        print(f"\033[94m{text}\033[00m", flush=True)
    except (UnicodeEncodeError, UnicodeDecodeError):
        clean_text = str(text).encode('ascii', 'ignore').decode('ascii')
        print(f"\033[94m{clean_text}\033[00m", flush=True)


def prPurple(text):
    """Imprime texto em roxo"""
    try:
        print(f"\033[95m{text}\033[00m", flush=True)
    except (UnicodeEncodeError, UnicodeDecodeError):
        clean_text = str(text).encode('ascii', 'ignore').decode('ascii')
        print(f"\033[95m{clean_text}\033[00m", flush=True)


def prCyan(text):
    """Imprime texto em ciano"""
    try:
        print(f"\033[96m{text}\033[00m", flush=True)
    except (UnicodeEncodeError, UnicodeDecodeError):
        clean_text = str(text).encode('ascii', 'ignore').decode('ascii')
        print(f"\033[96m{clean_text}\033[00m", flush=True)


def chromeBrowserOptions():
    """Retorna opções configuradas para o Chrome com perfil isolado"""
    import config
    
    options = webdriver.ChromeOptions()
    
    # Desabilitar notificações e popups
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Modo headless se configurado
    if config.headless:
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
    
    # USAR PERFIL ISOLADO NA PASTA DO PROJETO
    bot_profile_path = os.path.join(os.getcwd(), "selenium_profile")
    
    # Criar diretório se não existir
    if not os.path.exists(bot_profile_path):
        os.makedirs(bot_profile_path)
        prGreen(f"📁 Criando perfil isolado do Selenium em: {bot_profile_path}")
        prYellow("⚠️ Na primeira execução, você precisará fazer login no LinkedIn")
        prYellow("⚠️ O login será salvo neste perfil para as próximas execuções")
    else:
        prGreen(f"✅ Usando perfil isolado: {bot_profile_path}")
    
    options.add_argument(f"user-data-dir={bot_profile_path}")
    options.add_argument("--profile-directory=Default")
    
    # Evitar detecção de automação
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    return options


def firefoxBrowserOptions():
    """Retorna opções configuradas para o Firefox"""
    import config
    
    options = webdriver.FirefoxOptions()
    
    # Desabilitar notificações
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.push.enabled", False)
    
    # Modo headless se configurado
    if config.headless:
        options.add_argument("--headless")
    
    return options


def writeResults(text):
    """Escreve os resultados em um arquivo"""
    import config
    
    file_name = "Applied_Jobs_DATA_" + str(int(time.time()))
    file_name = file_name + config.outputFileType
    
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)
        prGreen(f"\n📄 Resultados salvos em: {file_name}")
    except Exception as e:
        prRed(f"\n❌ Erro ao salvar resultados: {str(e)}")


def getUrlDataFile():
    """Retorna o caminho do arquivo de URLs"""
    return "data/urlData.txt"


def jobExp(self):
    """Adiciona o filtro de nível de experiência à URL"""
    import config
    
    expLevels = config.experienceLevels
    if not expLevels:
        return ""
    
    jobExp = ""
    
    # Mapeamento com suporte para PORTUGUÊS e INGLÊS
    expMap = {
        # Inglês
        "Internship": "1",
        "Entry level": "2",
        "Associate": "3",
        "Mid-Senior level": "4",
        "Director": "5",
        "Executive": "6",
        
        # Português
        "Estágio": "1",
        "estagio": "1",
        "Assistente": "2",
        "assistente": "2",
        "Júnior": "2",
        "Junior": "2",
        "junior": "2",
        "júnior": "2",
        "Pleno": "4",
        "pleno": "4",
        "Pleno-sênior": "4",
        "Pleno-senior": "4",
        "pleno-senior": "4",
        "Sênior": "4",
        "Senior": "4",
        "senior": "4",
        "Diretor": "5",
        "diretor": "5",
        "Executivo": "6",
        "executivo": "6"
    }
    
    firstExp = expLevels[0]
    if firstExp in expMap:
        jobExp = f"&f_E={expMap[firstExp]}"
    
    for exp in expLevels[1:]:
        if exp in expMap:
            jobExp += f"%2C{expMap[exp]}"
    
    return jobExp


def datePosted(self):
    """Adiciona o filtro de data de postagem à URL"""
    import config
    
    dates = config.datePosted
    if not dates:
        return ""
    
    dateMap = {
        "Any Time": "",
        "Past Month": "&f_TPR=r2592000",
        "Past Week": "&f_TPR=r604800",
        "Past 24 hours": "&f_TPR=r86400"
    }
    
    date = dates[0]
    return dateMap.get(date, "")


def jobType(self):
    """Adiciona o filtro de tipo de trabalho à URL"""
    import config
    
    types = config.jobType
    if not types:
        return ""
    
    jobType = ""
    
    typeMap = {
        "Full-time": "F",
        "Part-time": "P",
        "Contract": "C",
        "Temporary": "T",
        "Volunteer": "V",
        "Internship": "I"
    }
    
    firstType = types[0]
    if firstType in typeMap:
        jobType = f"&f_JT={typeMap[firstType]}"
    
    for jType in types[1:]:
        if jType in typeMap:
            jobType += f"%2C{typeMap[jType]}"
    
    return jobType


def remote(self):
    """Adiciona o filtro de trabalho remoto à URL"""
    import config
    
    remoteTypes = config.remote
    if not remoteTypes:
        return ""
    
    remote = ""
    
    remoteMap = {
        "On-site": "1",
        "Remote": "2",
        "Hybrid": "3"
    }
    
    firstRemote = remoteTypes[0]
    if firstRemote in remoteMap:
        remote = f"&f_WT={remoteMap[firstRemote]}"
    
    for rType in remoteTypes[1:]:
        if rType in remoteMap:
            remote += f"%2C{remoteMap[rType]}"
    
    return remote


def salary(self):
    """Adiciona o filtro de salário à URL"""
    import config
    
    salaries = config.salary
    if not salaries or not salaries[0]:
        return ""
    
    salaryMap = {
        "40000": "1",
        "60000": "2",
        "80000": "3",
        "100000": "4",
        "120000": "5"
    }
    
    salary = salaries[0]
    if salary in salaryMap:
        return f"&f_SB2={salaryMap[salary]}"
    
    return ""


def sort(self):
    """Adiciona o filtro de ordenação à URL"""
    import config
    
    sorts = config.sort
    if not sorts:
        return ""
    
    sortMap = {
        "Recent": "&sortBy=DD",
        "Relevant": "&sortBy=R"
    }
    
    sort = sorts[0]
    return sortMap.get(sort, "")


class LinkedinUrlGenerate:
    """Classe para gerar URLs de busca do LinkedIn"""
    
    def __init__(self):
        pass
    
    def generateUrl(self, parameters, location):
        """Gera URL de busca com base nos parâmetros"""
        import config
        import urllib.parse  # ← ADICIONAR ESTA LINHA
        
        # URL base do LinkedIn Jobs
        url = "https://www.linkedin.com/jobs/search/?"
        
        # Adicionar localização
        if location:
            url += f"location={urllib.parse.quote(location)}"  # ← ESCAPAR
        
        # Adicionar palavras-chave
        if config.keywords:
            keywords_str = " ".join(config.keywords)
            # ESCAPAR CORRETAMENTE OS CARACTERES ESPECIAIS
            url += f"&keywords={urllib.parse.quote(keywords_str)}"  # ← MUDANÇA AQUI
        
        # Adicionar filtro Easy Apply
        url += "&f_AL=true"
        
        # Adicionar parâmetros adicionais
        url += parameters
        
        return url

    
    def generateUrls(self):
        """Gera todas as URLs de busca baseadas nas configurações"""
        import config
        
        urls = []
        
        # Gerar parâmetros de filtro
        parameters = ""
        parameters += jobExp(self)
        parameters += datePosted(self)
        parameters += jobType(self)
        parameters += remote(self)
        parameters += salary(self)
        parameters += sort(self)
        
        # Gerar URL para cada localização
        for location in config.location:
            url = self.generateUrl(parameters, location)
            urls.append(url)
        
        return urls
