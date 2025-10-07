# utils.py - Funções utilitárias para o bot
# Funções auxiliares usadas em todo o projeto

import math
import time
import config
import constants
from typing import List
from selenium import webdriver


def chromeBrowserOptions():
    """
    Configura as opções do navegador Chrome para o Selenium
    VERSÃO DE TESTE - SEM PERFIL
    """
    options = webdriver.ChromeOptions()
    
    # Argumentos essenciais
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('--remote-debugging-port=9222')
    
    # Desabilitar automação
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    
    prYellow("⚠️ MODO DE TESTE: Rodando SEM perfil (modo anônimo)")
    prYellow("⚠️ Você precisará fazer login manualmente no LinkedIn")
    
    return options


def firefoxBrowserOptions():
    """
    Configura as opções do navegador Firefox para o Selenium
    Retorna um objeto FirefoxOptions configurado
    """
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    
    options = FirefoxOptions()
    
    # Modo headless
    if config.headless:
        options.add_argument('--headless')
    
    # IMPORTANTE: Carregar perfil do Firefox se configurado
    if len(config.firefoxProfilePath) > 0:
        prYellow(f"🔧 Carregando perfil do Firefox: {config.firefoxProfilePath}")
        options.profile = config.firefoxProfilePath
    else:
        prYellow("⚠️ ATENÇÃO: Perfil do Firefox não configurado.")
        prYellow("⚠️ Para usar sem login, configure firefoxProfilePath no config.py")
    
    return options


def prRed(text):
    """Imprime texto em vermelho no terminal"""
    print(f"\033[91m{text}\033[00m")


def prGreen(text):
    """Imprime texto em verde no terminal"""
    print(f"\033[92m{text}\033[00m")


def prYellow(text):
    """Imprime texto em amarelo no terminal"""
    print(f"\033[93m{text}\033[00m")


def prBlue(text):
    """Imprime texto em azul no terminal"""
    print(f"\033[94m{text}\033[00m")


def getUrlDataFile():
    """
    Lê o arquivo com as URLs de busca geradas
    Retorna uma lista com as URLs
    """
    urlData = []
    try:
        with open('data/urlData.txt', 'r', encoding='utf-8') as file:
            urlData = file.readlines()
            urlData = [url.strip() for url in urlData if url.strip()]
    except FileNotFoundError:
        prRed("❌ Arquivo urlData.txt não encontrado na pasta /data")
        prRed("❌ Certifique-se de que a pasta 'data' existe e execute o bot novamente")
    return urlData


def jobsToPages(numOfJobs: str) -> int:
    """
    Converte o número total de vagas em número de páginas
    LinkedIn mostra 25 vagas por página
    """
    number_of_pages = 1
    
    if ' ' in numOfJobs:
        try:
            spaceIndex = numOfJobs.index(' ')
            totalJobs = numOfJobs[0:spaceIndex]
            totalJobs_int = int(totalJobs.replace(',', '').replace('.', ''))
            number_of_pages = math.ceil(totalJobs_int / constants.jobsPerPage)
            
            # LinkedIn limita a busca em aproximadamente 40 páginas
            if number_of_pages > constants.maxPages:
                number_of_pages = constants.maxPages
                prYellow(f"⚠️ Limitando busca a {constants.maxPages} páginas (limite do LinkedIn)")
        except:
            number_of_pages = 1
    else:
        try:
            number_of_pages = int(numOfJobs)
        except:
            number_of_pages = 1
    
    return number_of_pages


def urlToKeywords(url: str) -> List[str]:
    """
    Extrai as palavras-chave e localização de uma URL de busca
    Retorna [keyword, location]
    """
    try:
        keywordUrl = url[url.index("keywords=") + 9:]
        keyword = keywordUrl[0:keywordUrl.index("&")]
        
        locationUrl = url[url.index("location=") + 9:]
        location = locationUrl[0:locationUrl.index("&")]
        
        return [keyword, location]
    except:
        return ["Desconhecido", "Desconhecido"]


def writeResults(text: str):
    """
    Escreve os resultados das candidaturas em um arquivo .txt ou .csv
    """
    timeStr = time.strftime("%Y%m%d")
    
    # Determinar extensão do arquivo
    extension = config.outputFileType if config.outputFileType in [".txt", ".csv"] else ".txt"
    fileName = f"Candidaturas_Aplicadas_{timeStr}{extension}"
    filePath = f"data/{fileName}"
    
    try:
        # Tentar ler arquivo existente
        with open(filePath, 'r', encoding='utf-8') as file:
            lines = []
            for line in file:
                if "----" not in line:
                    lines.append(line)
        
        # Reescrever com novo conteúdo
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(f"---- Dados de Candidaturas Aplicadas ---- criado em: {timeStr}\n")
            f.write("---- Número | Título da Vaga | Empresa | Localização | Modalidade | Data Postagem | Candidaturas | Resultado\n")
            for line in lines:
                f.write(line)
            f.write(text + "\n")
    
    except FileNotFoundError:
        # Criar novo arquivo
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(f"---- Dados de Candidaturas Aplicadas ---- criado em: {timeStr}\n")
            f.write("---- Número | Título da Vaga | Empresa | Localização | Modalidade | Data Postagem | Candidaturas | Resultado\n")
            f.write(text + "\n")


class LinkedinUrlGenerate:
    """
    Classe responsável por gerar as URLs de busca do LinkedIn
    baseadas nas configurações do config.py
    """
    
    def generateUrlLinks(self):
        """
        Gera todas as combinações de URLs baseadas em:
        - Localizações configuradas
        - Palavras-chave configuradas
        - Filtros aplicados
        """
        urls = []
        
        for location in config.location:
            for keyword in config.keywords:
                url = (
                    constants.linkJobUrl + 
                    "?f_AL=true" +  # Easy Apply apenas
                    "&keywords=" + keyword +
                    self.jobType() +
                    self.remote() +
                    self.checkJobLocation(location) +
                    self.jobExp() +
                    self.datePosted() +
                    self.salary() +
                    self.sortBy()
                )
                urls.append(url)
        
        return urls
    
    def checkJobLocation(self, job):
        """Adiciona o filtro de localização à URL"""
        jobLoc = "&location=" + job
        
        # IDs geográficos do LinkedIn para continentes
        match job.casefold():
            case "asia":
                jobLoc += "&geoId=102393603"
            case "europe":
                jobLoc += "&geoId=100506914"
            case "northamerica":
                jobLoc += "&geoId=102221843"
            case "southamerica":
                jobLoc += "&geoId=104514572"
            case "australia":
                jobLoc += "&geoId=101452733"
            case "africa":
                jobLoc += "&geoId=103537801"
        
        return jobLoc
    
    def jobExp(self):
        """Adiciona o filtro de nível de experiência à URL"""
        expLevels = config.experienceLevels
        if not expLevels:
            return ""
        
        jobExp = ""
        expMap = {
            "Internship": "1",
            "Entry level": "2",
            "Associate": "3",
            "Mid-Senior level": "4",
            "Director": "5",
            "Executive": "6"
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
        if not config.datePosted:
            return ""
        
        dateMap = {
            "Any Time": "",
            "Past Month": "&f_TPR=r2592000",
            "Past Week": "&f_TPR=r604800",
            "Past 24 hours": "&f_TPR=r86400"
        }
        
        return dateMap.get(config.datePosted[0], "")
    
    def jobType(self):
        """Adiciona o filtro de tipo de trabalho à URL"""
        jobTypes = config.jobType
        if not jobTypes:
            return ""
        
        typeMap = {
            "Full-time": "F",
            "Part-time": "P",
            "Contract": "C",
            "Temporary": "T",
            "Volunteer": "V",
            "Internship": "I",
            "Other": "O"
        }
        
        jobType = ""
        firstType = jobTypes[0]
        if firstType in typeMap:
            jobType = f"&f_JT={typeMap[firstType]}"
        
        for jType in jobTypes[1:]:
            if jType in typeMap:
                jobType += f"%2C{typeMap[jType]}"
        
        return jobType + "&" if jobType else ""
    
    def remote(self):
        """Adiciona o filtro de modalidade de trabalho à URL"""
        remoteTypes = config.remote
        if not remoteTypes:
            return ""
        
        remoteMap = {
            "On-site": "1",
            "Remote": "2",
            "Hybrid": "3"
        }
        
        jobRemote = ""
        firstRemote = remoteTypes[0]
        if firstRemote in remoteMap:
            jobRemote = f"f_WT={remoteMap[firstRemote]}"
        
        for rType in remoteTypes[1:]:
            if rType in remoteMap:
                jobRemote += f"%2C{remoteMap[rType]}"
        
        return jobRemote
    
    def salary(self):
        """Adiciona o filtro de salário à URL"""
        if not config.salary or config.salary[0] == "":
            return ""
        
        salaryMap = {
            "$40,000+": "1",
            "$60,000+": "2",
            "$80,000+": "3",
            "$100,000+": "4",
            "$120,000+": "5",
            "$140,000+": "6",
            "$160,000+": "7",
            "$180,000+": "8",
            "$200,000+": "9"
        }
        
        salaryValue = config.salary[0]
        if salaryValue in salaryMap:
            return f"f_SB2={salaryMap[salaryValue]}&"
        
        return ""
    
    def sortBy(self):
        """Adiciona o filtro de ordenação à URL"""
        if not config.sort:
            return "sortBy=R"  # Relevante por padrão
        
        sortMap = {
            "Recent": "sortBy=DD",
            "Relevant": "sortBy=R"
        }
        
        return sortMap.get(config.sort[0], "sortBy=R")
