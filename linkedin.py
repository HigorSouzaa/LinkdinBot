# -*- coding: utf-8 -*-
"""
LinkedIn Easy Apply Bot
Versão: 1.0.0
"""

import sys
import os

# Forçar UTF-8 no Windows para suportar emojis
if sys.platform == "win32":
    try:
        # Mudar codepage do console para UTF-8
        os.system("chcp 65001 > nul 2>&1")
        # Reconfigurar stdout e stderr
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# Imports principais
import time
import math
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Imports do projeto
import utils
import constants
import config

# Para Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# Para Firefox (caso queira usar)
try:
    from webdriver_manager.firefox import GeckoDriverManager
    from selenium.webdriver.firefox.service import Service as FirefoxService
except:
    pass


class LinkedinBot:
    """
    Classe principal do bot de aplicação automática no LinkedIn
    """
    
    def __init__(self):
        """
        Inicializa o bot e configura o navegador
        """
        utils.prBlue("=" * 60)
        utils.prBlue(constants.projectName)
        utils.prBlue(f"Versão: {constants.version}")
        utils.prBlue("=" * 60)
        utils.prYellow(constants.welcomeMessage)
        
        
        # Verificar se o perfil do navegador está configurado
        self.checkProfileConfiguration()
        
        # Inicializar navegador
        self.driver = self.initBrowser()
        
        # Verificar se está logado
        if not self.isLoggedIn():
            utils.prRed("❌ ERRO: Você não está logado no LinkedIn!")
            utils.prRed("❌ Por favor, configure o perfil do navegador no config.py")
            utils.prRed("❌ O perfil deve estar previamente logado no LinkedIn")
            self.driver.quit()
            sys.exit(1)
        
        utils.prGreen("✅ Login verificado com sucesso!")
        
        # Iniciar processo de candidaturas
        self.startApplying()
    
    def checkProfileConfiguration(self):
        """
        Verifica se o perfil do navegador está configurado
        """
        if config.browser == "Chrome":
            if not config.chromeProfilePath or config.chromeProfilePath == "":
                utils.prRed("=" * 60)
                utils.prRed("⚠️  ATENÇÃO: Perfil do Chrome não configurado!")
                utils.prRed("=" * 60)
                utils.prYellow("Para usar o bot sem credenciais, você precisa:")
                utils.prYellow("1. Abrir o Chrome e fazer login no LinkedIn")
                utils.prYellow("2. Digitar chrome://version/ na barra de endereços")
                utils.prYellow("3. Copiar o 'Caminho do perfil' (sem o nome do perfil no final)")
                utils.prYellow("4. Colar no config.py na variável chromeProfilePath")
                utils.prYellow("5. Configurar chromeProfileName (ex: 'Default', 'Profile 1', etc)")
                utils.prRed("=" * 60)
                
                response = input("\n⚠️  Deseja continuar mesmo assim? (s/n): ").lower()
                if response != 's':
                    sys.exit(0)
        
        elif config.browser == "Firefox":
            if not config.firefoxProfilePath or config.firefoxProfilePath == "":
                utils.prRed("=" * 60)
                utils.prRed("⚠️  ATENÇÃO: Perfil do Firefox não configurado!")
                utils.prRed("=" * 60)
                utils.prYellow("Para usar o bot sem credenciais, você precisa:")
                utils.prYellow("1. Abrir o Firefox e fazer login no LinkedIn")
                utils.prYellow("2. Digitar about:profiles na barra de endereços")
                utils.prYellow("3. Copiar o 'Diretório raiz' do perfil que está usando")
                utils.prYellow("4. Colar no config.py na variável firefoxProfilePath")
                utils.prRed("=" * 60)
                
                response = input("\n⚠️  Deseja continuar mesmo assim? (s/n): ").lower()
                if response != 's':
                    sys.exit(0)
    
    def initBrowser(self):
        """
        Inicializa o navegador (Chrome ou Firefox) com as configurações
        """
        utils.prYellow(f"🌐 Inicializando navegador {config.browser}...")
        
        try:
            if config.browser == "Chrome":
                options = utils.chromeBrowserOptions()
                driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
                utils.prGreen("✅ Chrome inicializado com sucesso!")
                
            elif config.browser == "Firefox":
                options = utils.firefoxBrowserOptions()
                driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )
                utils.prGreen("✅ Firefox inicializado com sucesso!")
            
            else:
                utils.prRed(f"❌ Navegador '{config.browser}' não suportado!")
                utils.prRed("❌ Use 'Chrome' ou 'Firefox' no config.py")
                sys.exit(1)
            
            return driver
            
        except Exception as e:
            utils.prRed(f"❌ Erro ao inicializar navegador: {str(e)}")
            sys.exit(1)
    
    def isLoggedIn(self):
        """
        Verifica se o usuário está logado no LinkedIn
        Retorna True se estiver logado, False caso contrário
        """
        utils.prYellow("🔍 Verificando se está logado no LinkedIn...")
        
        try:
            self.driver.get(constants.linkedinFeedUrl)
            time.sleep(10)  # Aguardar carregar
            
            # Verificar se está na página de login
            current_url = self.driver.current_url
            
            if "login" in current_url or "authwall" in current_url:
                utils.prYellow("\n⚠️  Você NÃO está logado no LinkedIn")
                utils.prYellow("⚠️  Por favor, faça login AGORA na janela do Chrome que abriu")
                utils.prYellow("⚠️  Você tem 60 segundos para fazer o login...\n")
                
                # Aguardar 180 segundos para o usuário fazer login
                for i in range(360, 0, -5):
                    utils.prYellow(f"⏰ Aguardando login... {i} segundos restantes")
                    time.sleep(5)
                    
                    # Verificar se já logou
                    current_url = self.driver.current_url
                    if "feed" in current_url or "linkedin.com/feed" in current_url:
                        utils.prGreen("\n✅ Login detectado com sucesso!")
                        return True
                
                # Verificar uma última vez
                self.driver.get(constants.linkedinFeedUrl)
                time.sleep(3)
                current_url = self.driver.current_url
                
                if "login" in current_url or "authwall" in current_url:
                    return False
                else:
                    return True
            
            # Já está logado
            if "feed" in current_url:
                return True
            
            # Tentar encontrar elementos que só aparecem quando logado
            try:
                # Procurar pela barra de navegação do feed
                self.driver.find_element(By.XPATH, "//nav[contains(@class, 'global-nav')]")
                return True
            except:
                pass
            
            # Tentar outro método: verificar se existe o botão de "Start a post"
            try:
                self.driver.find_element(By.XPATH, "//button[contains(@class, 'share-box')]")
                return True
            except:
                pass
            
            return False
            
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Erro ao verificar login: {str(e)}")
            return False

    
    def generateUrls(self):
        """Gera as URLs de busca baseadas nas configurações e salva em um arquivo data/urlData.txt"""
        utils.prYellow("🔗 Gerando URLs de busca...")
        
        # Criar pasta data se não existir
        if not os.path.exists("data"):
            os.makedirs("data")
            utils.prGreen("📁 Pasta data criada")
        
        try:
            # Criar instância do gerador de URLs
            url_generator = utils.LinkedinUrlGenerate()
            urls = url_generator.generateUrls()
            
            # Salvar URLs no arquivo
            with open("data/urlData.txt", "w", encoding="utf-8") as file:
                for url in urls:
                    file.write(url + "\n")
            
            utils.prGreen(f"✅ {len(urls)} URLs de busca criadas com sucesso!")
            utils.prYellow(f"📍 Combinações: {len(config.location)} localizações × {len(config.keywords)} palavras-chave")
            
        except Exception as e:
            utils.prRed(f"❌ Erro ao gerar URLs: {str(e)}")
            utils.prRed("❌ Verifique as configurações no config.py (linhas de location e keywords)")
            sys.exit(1)

    
    def start(self):
        """Inicia o processo de aplicação automática"""
        utils.prBlue("\n" + "="*60)
        utils.prBlue("🚀 INICIANDO PROCESSO DE CANDIDATURAS")
        utils.prBlue("="*60 + "\n")
        
        # Ler URLs do arquivo
        urlData = []
        try:
            with open(utils.getUrlDataFile(), 'r', encoding='utf-8') as file:
                urlData = [line.strip() for line in file.readlines() if line.strip()]
            
            if not urlData:
                utils.prRed("❌ Nenhuma URL encontrada no arquivo!")
                return
            
            utils.prYellow(f"📍 Total de URLs para processar: {len(urlData)}\n")
            
        except FileNotFoundError:
            utils.prRed(f"❌ Arquivo {utils.getUrlDataFile()} não encontrado!")
            return
        except Exception as e:
            utils.prRed(f"❌ Erro ao ler arquivo de URLs: {str(e)}")
            return
        
        # PROCESSAR CADA URL (NÃO MULTIPLICAR!)
        for urlIndex, url in enumerate(urlData):
            utils.prYellow(f"\n📍 Processando URL {urlIndex + 1}/{len(urlData)}")
            
            # VALIDAR SE É UMA URL VÁLIDA
            if not url or not url.startswith('http'):
                utils.prRed(f"❌ URL inválida pulada: {url[:100] if url else 'vazio'}")
                continue
            
            utils.prCyan(f"🔗 URL: {url}")
            
            try:
                # Navegar para a URL
                self.driver.get(url)
                time.sleep(random.uniform(3, 5))
                
                # PROCESSAR VAGAS DESTA URL
                self.processJobListings()
                
            except Exception as e:
                utils.prRed(f"❌ Erro ao processar URL: {str(e)}")
                continue
        
        # Resumo final
        self.finish()

    def processJobListings(self):
        """Processa todas as vagas da página atual"""
        try:
            # Aguardar carregamento das vagas
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search__results-list"))
            )
            
            # Encontrar todas as vagas
            job_listings = self.driver.find_elements(By.CSS_SELECTOR, "li.jobs-search-results__list-item")
            
            utils.prGreen(f"✅ Encontradas {len(job_listings)} vagas nesta busca")
            
            for index, job in enumerate(job_listings, 1):
                try:
                    # Rolar até a vaga
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", job)
                    time.sleep(1)
                    
                    # Clicar na vaga
                    job.click()
                    time.sleep(random.uniform(2, 3))
                    
                    # Tentar aplicar
                    self.easyApply()
                    
                except Exception as e:
                    utils.prRed(f"❌ Erro na vaga {index}: {str(e)}")
                    continue
            
        except TimeoutException:
            utils.prRed("❌ Timeout ao carregar vagas")
        except Exception as e:
            utils.prRed(f"❌ Erro ao processar vagas: {str(e)}")


    def getJobProperties(self, count):
        """
        Extrai as propriedades/informações de uma vaga
        Retorna string formatada com as informações
        """
        jobTitle = ""
        jobCompany = ""
        jobLocation = ""
        jobDetails = ""
        
        # Obter título da vaga (múltiplas tentativas)
        try:
            # Tentativa 1: h1 com classe específica
            try:
                jobTitleElement = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job') or contains(@class, 'title') or contains(@class, 't-24')]")
                jobTitle = jobTitleElement.text.strip()
            except:
                pass
            
            # Tentativa 2: Qualquer h1 visível
            if not jobTitle:
                try:
                    h1Elements = self.driver.find_elements(By.TAG_NAME, "h1")
                    for h1 in h1Elements:
                        if h1.is_displayed() and len(h1.text.strip()) > 3:
                            jobTitle = h1.text.strip()
                            break
                except:
                    pass
            
            # Tentativa 3: Por classe específica do LinkedIn
            if not jobTitle:
                try:
                    jobTitleElement = self.driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__job-title")
                    jobTitle = jobTitleElement.text.strip()
                except:
                    pass
            
            if not jobTitle:
                jobTitle = "Título não encontrado"
            
            # Verificar blacklist de títulos
            for blacklistedTitle in config.blackListTitles:
                if blacklistedTitle.lower() in jobTitle.lower():
                    jobTitle += f" (BLACKLISTED: {blacklistedTitle})"
                    break
                    
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Erro ao obter título: {str(e)[:50]}")
            jobTitle = "Título não encontrado"
        
        # Obter detalhes da vaga (empresa, localização, etc)
        try:
            time.sleep(1)
            
            # Procurar detalhes da vaga
            try:
                jobDetailsElement = self.driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__primary-description")
                jobDetails = jobDetailsElement.text.replace("\n", " | ")
            except:
                try:
                    jobDetailsElement = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details') or contains(@class, 'jobs-unified')]")
                    jobDetails = jobDetailsElement.text.replace("\n", " | ")
                except:
                    jobDetails = ""
            
            # Verificar blacklist de empresas
            for blacklistedCompany in config.blacklistCompanies:
                if blacklistedCompany.lower() in jobDetails.lower():
                    jobDetails += f" (BLACKLISTED COMPANY: {blacklistedCompany})"
                    break
                    
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Erro ao obter detalhes: {str(e)[:50]}")
            jobDetails = "Detalhes não encontrados"
        
        # Obter informações de modalidade (remoto, híbrido, presencial)
        try:
            workModeElements = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'ui-label') or contains(@class, 'workplace-type')]")
            for element in workModeElements:
                try:
                    if element.is_displayed():
                        jobLocation += " | " + element.text
                except:
                    pass
        except:
            pass
        
        textToWrite = f"{count} | {jobTitle} | {jobDetails}{jobLocation}"
        return textToWrite

    
    def checkWhitelist(self, jobProperties):
        """
        Verifica se a vaga atende aos critérios de whitelist
        Retorna True se atender, False caso contrário
        """
        jobPropertiesLower = jobProperties.lower()
        
        # Verificar whitelist de empresas
        if config.onlyApplyCompanies:
            foundCompany = False
            for company in config.onlyApplyCompanies:
                if company.lower() in jobPropertiesLower:
                    foundCompany = True
                    break
            if not foundCompany:
                return False
        
        # Verificar whitelist de títulos
        if config.onlyApplyTitles:
            foundTitle = False
            for title in config.onlyApplyTitles:
                if title.lower() in jobPropertiesLower:
                    foundTitle = True
                    break
            if not foundTitle:
                return False
        
        return True
    
    def applyToJob(self, offerPage):
        """
        Tenta aplicar para uma vaga
        Retorna: 'applied', 'already_applied', ou 'failed'
        """
        try:
            # Aguardar página carregar
            time.sleep(random.uniform(2, 3))
            
            # Verificar se o botão Easy Apply existe
            easyApplyButton = self.findEasyApplyButton()
            
            if easyApplyButton is None:
                if config.displayWarnings:
                    utils.prYellow("  ⚠️ Botão Easy Apply não encontrado")
                return "failed"
            
            if easyApplyButton == "already_applied":
                return "already_applied"
            
            # Tentar clicar no botão Easy Apply de várias formas
            clicked = False
            
            # Método 1: Click normal
            try:
                easyApplyButton.click()
                clicked = True
            except:
                pass
            
            # Método 2: JavaScript click
            if not clicked:
                try:
                    self.driver.execute_script("arguments[0].click();", easyApplyButton)
                    clicked = True
                except:
                    pass
            
            # Método 3: ActionChains
            if not clicked:
                try:
                    from selenium.webdriver.common.action_chains import ActionChains
                    actions = ActionChains(self.driver)
                    actions.move_to_element(easyApplyButton).click().perform()
                    clicked = True
                except:
                    pass
            
            if not clicked:
                if config.displayWarnings:
                    utils.prYellow("  ⚠️ Não foi possível clicar no botão Easy Apply")
                return "failed"
            
            # Aguardar modal abrir
            time.sleep(random.uniform(2, config.botSpeed))
            
            # Salvar vaga antes de aplicar (se configurado)
            if config.saveBeforeApply:
                try:
                    saveButton = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Save') or contains(@aria-label, 'Salvar')]")
                    if "saved" not in saveButton.get_attribute("aria-label").lower():
                        saveButton.click()
                        time.sleep(0.5)
                except:
                    pass
            
            # Tentar aplicação simples (sem etapas adicionais)
            try:
                self.chooseResume()
                time.sleep(1)
                
                # Procurar botão de enviar
                submitButtons = self.driver.find_elements(By.XPATH, "//button[contains(@aria-label, 'Submit application') or contains(@aria-label, 'Enviar candidatura')]")
                
                for submitBtn in submitButtons:
                    if submitBtn.is_displayed() and submitBtn.is_enabled():
                        try:
                            submitBtn.click()
                        except:
                            self.driver.execute_script("arguments[0].click();", submitBtn)
                        
                        time.sleep(random.uniform(1, config.botSpeed))
                        return "applied"
            
            except:
                pass
            
            # Se não conseguiu aplicação simples, tentar aplicação com múltiplas etapas
            try:
                return self.applyMultiStep(offerPage)
            except Exception as e:
                if config.displayWarnings:
                    utils.prYellow(f"  ⚠️ Erro na aplicação: {str(e)[:100]}")
                return "failed"
        
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"  ⚠️ Erro geral ao aplicar: {str(e)[:100]}")
            return "failed"

    
    def findEasyApplyButton(self):
        """
        Procura o botão Easy Apply / Candidatura simplificada na página
        Retorna o elemento do botão, 'already_applied', ou None
        """
        try:
            # Aguardar a página carregar completamente
            time.sleep(random.uniform(2, 3))
            
            # Verificar se já aplicou anteriormente (textos em português e inglês)
            try:
                appliedTexts = [
                    "Applied", "Candidatou-se", "Você já se candidatou",
                    "Application sent", "Candidatura enviada"
                ]
                
                for text in appliedTexts:
                    appliedElements = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
                    for elem in appliedElements:
                        try:
                            if elem.is_displayed():
                                return "already_applied"
                        except:
                            pass
            except:
                pass
            
            # Scroll para garantir que o botão esteja visível
            try:
                self.driver.execute_script("window.scrollTo(0, 500);")
                time.sleep(1)
            except:
                pass
            
            # Procurar botão Easy Apply / Candidatura simplificada com múltiplas estratégias
            button = None
            
            # Lista de textos possíveis do botão (português e inglês)
            buttonTexts = [
                "Candidatura simplificada",
                "Easy Apply",
                "Candidatar-se",
                "Apply"
            ]
            
            # Estratégia 1: Procurar por qualquer um dos textos possíveis
            for buttonText in buttonTexts:
                try:
                    buttons = self.driver.find_elements(By.XPATH, f"//button[contains(., '{buttonText}')]")
                    for btn in buttons:
                        try:
                            if btn.is_displayed() and btn.is_enabled():
                                # Verificar se realmente é o botão de aplicação
                                btnClass = btn.get_attribute("class") or ""
                                if "jobs-apply-button" in btnClass or "artdeco-button" in btnClass:
                                    button = btn
                                    utils.prGreen(f"  ✅ Botão encontrado: '{buttonText}'")
                                    break
                        except:
                            pass
                    if button:
                        break
                except:
                    pass
            
            # Estratégia 2: Procurar pela classe específica do botão
            if not button:
                try:
                    buttons = self.driver.find_elements(By.CSS_SELECTOR, "button.jobs-apply-button")
                    for btn in buttons:
                        try:
                            if btn.is_displayed() and btn.is_enabled():
                                button = btn
                                utils.prGreen(f"  ✅ Botão encontrado pela classe CSS")
                                break
                        except:
                            pass
                except:
                    pass
            
            # Estratégia 3: Procurar por aria-label
            if not button:
                try:
                    for buttonText in buttonTexts:
                        buttons = self.driver.find_elements(By.XPATH, f"//button[contains(@aria-label, '{buttonText}')]")
                        for btn in buttons:
                            try:
                                if btn.is_displayed() and btn.is_enabled():
                                    button = btn
                                    utils.prGreen(f"  ✅ Botão encontrado por aria-label: '{buttonText}'")
                                    break
                            except:
                                pass
                        if button:
                            break
                except:
                    pass
            
            # Se encontrou o botão, rolar até ele e aguardar
            if button:
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                    time.sleep(1)
                except:
                    pass
                return button
            
            # Se não encontrou, tentar procurar o texto exato na imagem que você mandou
            if not button:
                try:
                    # Procurar especificamente pelo texto "Candidatura simplificada" com ícone
                    buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'jobs-apply-button') or contains(@class, 'artdeco-button--primary')]")
                    for btn in buttons:
                        try:
                            btnText = btn.text.strip()
                            if any(text in btnText for text in buttonTexts):
                                if btn.is_displayed() and btn.is_enabled():
                                    button = btn
                                    utils.prGreen(f"  ✅ Botão encontrado pelo texto: '{btnText}'")
                                    break
                        except:
                            pass
                except:
                    pass
            
            return button if button else None
            
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"⚠️ Erro ao procurar botão: {str(e)}")
            return None

        
    def chooseResume(self):
        """
        Seleciona o currículo preferido (se necessário)
        """
        try:
            # Verificar se precisa selecionar currículo
            self.driver.find_element(By.CLASS_NAME, "jobs-document-upload__title--is-required")
            
            # Obter lista de currículos
            resumes = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'ui-attachment--pdf')]")
            
            if len(resumes) == 0:
                utils.prRed("  ❌ Nenhum currículo encontrado no LinkedIn!")
                utils.prRed("  ❌ Adicione pelo menos um currículo à sua conta")
                return
            
            # Selecionar currículo baseado na preferência
            cvIndex = config.preferredCv - 1
            if cvIndex < len(resumes):
                if resumes[cvIndex].get_attribute("aria-label") == "Select this resume":
                    resumes[cvIndex].click()
                    time.sleep(0.5)
            else:
                # Se o índice preferido não existe, usar o primeiro
                if resumes[0].get_attribute("aria-label") == "Select this resume":
                    resumes[0].click()
                    time.sleep(0.5)
        
        except:
            # Não é necessário selecionar currículo
            pass
    
    def applyMultiStep(self, offerPage):
        """
        Aplica para vagas com múltiplas etapas e perguntas adicionais
        Retorna 'applied' ou 'failed'
        """
        try:
            utils.prYellow("  📝 Processando candidatura com múltiplas etapas...")
            
            maxSteps = 10  # Máximo de etapas para evitar loop infinito
            currentStep = 0
            
            while currentStep < maxSteps:
                currentStep += 1
                time.sleep(random.uniform(1, 2))
                
                # Verificar se chegou na tela de revisão final
                try:
                    reviewButtons = self.driver.find_elements(By.XPATH, 
                        "//button[contains(@aria-label, 'Rever') or contains(@aria-label, 'Review') or contains(., 'Rever sua candidatura') or contains(., 'Review your application')]")
                    
                    for btn in reviewButtons:
                        if btn.is_displayed() and btn.is_enabled():
                            utils.prGreen(f"  ✅ Chegou na revisão final (etapa {currentStep})")
                            
                            try:
                                btn.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", btn)
                            
                            time.sleep(2)
                            
                            # Desmarcar "seguir empresa" se configurado
                            if not config.followCompanies:
                                try:
                                    followCheckboxes = self.driver.find_elements(By.XPATH, 
                                        "//label[contains(@for, 'follow-company')]")
                                    for checkbox in followCheckboxes:
                                        if checkbox.is_displayed():
                                            checkbox.click()
                                            time.sleep(0.5)
                                except:
                                    pass
                            
                            # Enviar candidatura final
                            return self.submitFinalApplication()
                except:
                    pass
                
                # Verificar se já foi enviada (às vezes aparece mensagem de sucesso)
                try:
                    successTexts = ["enviada", "sent", "submetida", "submitted"]
                    for text in successTexts:
                        elements = self.driver.find_elements(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{text}')]")
                        for elem in elements:
                            if elem.is_displayed() and ("candidatura" in elem.text.lower() or "application" in elem.text.lower()):
                                utils.prGreen("  ✅ Candidatura enviada com sucesso!")
                                return "applied"
                except:
                    pass
                
                # Escolher currículo se necessário
                self.chooseResume()
                time.sleep(1)
                
                # Tentar preencher perguntas automáticas
                self.answerQuestions()
                time.sleep(1)
                
                # Procurar botão "Avançar" / "Continue" / "Próximo"
                continueButton = None
                continueTexts = [
                    "Avançar",
                    "Próximo",
                    "Continue",
                    "Next",
                    "Continuar"
                ]
                
                for btnText in continueTexts:
                    try:
                        buttons = self.driver.find_elements(By.XPATH, f"//button[contains(., '{btnText}')]")
                        for btn in buttons:
                            if btn.is_displayed() and btn.is_enabled():
                                btnAriaLabel = btn.get_attribute("aria-label") or ""
                                if "next step" in btnAriaLabel.lower() or "próxima etapa" in btnAriaLabel.lower() or len(btnAriaLabel) == 0:
                                    continueButton = btn
                                    break
                        if continueButton:
                            break
                    except:
                        pass
                
                # Se encontrou botão de continuar, clicar
                if continueButton:
                    try:
                        utils.prYellow(f"  ⏩ Avançando para próxima etapa ({currentStep}/{maxSteps})")
                        continueButton.click()
                    except:
                        self.driver.execute_script("arguments[0].click();", continueButton)
                    
                    time.sleep(random.uniform(1, 2))
                    continue
                
                # Se não encontrou botão de continuar, tentar enviar diretamente
                submitResult = self.submitFinalApplication()
                if submitResult == "applied":
                    return "applied"
                
                # Se chegou aqui e não conseguiu avançar, pode estar travado
                utils.prYellow(f"  ⚠️ Não encontrou botão para avançar na etapa {currentStep}")
                
                # Última tentativa: procurar qualquer botão primário
                try:
                    primaryButtons = self.driver.find_elements(By.CSS_SELECTOR, "button.artdeco-button--primary")
                    for btn in primaryButtons:
                        if btn.is_displayed() and btn.is_enabled():
                            btnText = btn.text.strip()
                            if len(btnText) > 0 and btnText.lower() not in ["fechar", "close", "cancelar", "cancel"]:
                                utils.prYellow(f"  🔄 Tentando clicar em: '{btnText}'")
                                try:
                                    btn.click()
                                except:
                                    self.driver.execute_script("arguments[0].click();", btn)
                                time.sleep(2)
                                break
                except:
                    pass
                
                # Se passou de 5 etapas sem sucesso, desistir
                if currentStep >= 5:
                    utils.prYellow(f"  ⚠️ Muitas etapas ({currentStep}), pulando esta vaga")
                    break
            
            return "failed"
            
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"  ⚠️ Erro na aplicação multi-step: {str(e)[:150]}")
            return "failed"


    def answerQuestions(self):
        """
        Tenta responder perguntas automáticas do formulário usando dados do config
        """
        try:
            if not config.autoFillEnabled:
                return
            
            # Procurar campos de texto vazios e preencher com valores do config
            textInputs = self.driver.find_elements(By.XPATH, "//input[@type='text' or @type='number']")
            for inp in textInputs:
                try:
                    if inp.is_displayed() and inp.is_enabled():
                        currentValue = inp.get_attribute("value") or ""
                        if len(currentValue.strip()) == 0:
                            # Verificar o label para saber o que preencher
                            inputId = inp.get_attribute("id") or ""
                            placeholder = inp.get_attribute("placeholder") or ""
                            labelText = ""
                            
                            if inputId:
                                try:
                                    label = self.driver.find_element(By.XPATH, f"//label[@for='{inputId}']")
                                    labelText = label.text.lower()
                                except:
                                    pass
                            
                            # Combinar label e placeholder para melhor detecção
                            fullText = (labelText + " " + placeholder.lower()).strip()
                            
                            # Preencher baseado no tipo de pergunta usando dados do config
                            filled = False
                            
                            # Anos de experiência
                            if any(word in fullText for word in ["anos", "years", "experiência", "experience", "tempo"]):
                                inp.send_keys(config.personalInfo["yearsOfExperience"])
                                filled = True
                            
                            # Salário
                            elif any(word in fullText for word in ["salário", "salary", "pretensão", "remuneração", "compensação"]):
                                inp.send_keys(config.personalInfo["salaryExpectation"])
                                filled = True
                            
                            # Salário por hora
                            elif any(word in fullText for word in ["hora", "hour", "hourly"]):
                                inp.send_keys(config.personalInfo["hourlyRate"])
                                filled = True
                            
                            # Telefone
                            elif any(word in fullText for word in ["telefone", "phone", "celular", "contato", "whatsapp"]):
                                inp.send_keys(config.personalInfo["phone"])
                                filled = True
                            
                            # Cidade
                            elif any(word in fullText for word in ["cidade", "city", "localização", "location"]):
                                inp.send_keys(config.personalInfo["city"])
                                filled = True
                            
                            # País
                            elif any(word in fullText for word in ["país", "country", "nacionalidade"]):
                                inp.send_keys(config.personalInfo["country"])
                                filled = True
                            
                            # Disponibilidade
                            elif any(word in fullText for word in ["disponibilidade", "availability", "início", "start"]):
                                inp.send_keys(config.personalInfo["availability"])
                                filled = True
                            
                            # LinkedIn
                            elif any(word in fullText for word in ["linkedin", "perfil"]):
                                if config.personalInfo["linkedinUrl"]:
                                    inp.send_keys(config.personalInfo["linkedinUrl"])
                                    filled = True
                            
                            # Portfolio/GitHub
                            elif any(word in fullText for word in ["portfolio", "github", "site", "website"]):
                                if config.personalInfo["portfolioUrl"]:
                                    inp.send_keys(config.personalInfo["portfolioUrl"])
                                    filled = True
                            
                            # Idiomas
                            elif any(word in fullText for word in ["idioma", "língua", "language", "inglês", "english"]):
                                inp.send_keys(config.personalInfo["englishLevel"])
                                filled = True
                            
                            if filled:
                                time.sleep(0.3)
                                
                except:
                    pass
            
            # Selecionar primeira opção em dropdowns (se habilitado)
            if config.autoSelectFirstOption:
                try:
                    selects = self.driver.find_elements(By.TAG_NAME, "select")
                    for select in selects:
                        if select.is_displayed():
                            try:
                                options = select.find_elements(By.TAG_NAME, "option")
                                if len(options) > 1:  # Se tem opções além da padrão
                                    options[1].click()  # Selecionar segunda opção (primeira real)
                                    time.sleep(0.5)
                            except:
                                pass
                except:
                    pass
            
            # Marcar checkboxes de "Sim" se habilitado
            if config.autoSelectYes:
                try:
                    # Procurar por radio buttons com "Sim" ou "Yes"
                    yesRadios = self.driver.find_elements(By.XPATH, 
                        "//input[@type='radio' and (contains(@value, 'Yes') or contains(@value, 'Sim') or contains(@value, 'yes') or contains(@value, 'sim') or @value='1' or @value='true')]")
                    for radio in yesRadios:
                        try:
                            if radio.is_displayed() and not radio.is_selected():
                                # Verificar se o label contém "sim" ou "yes"
                                radioId = radio.get_attribute("id") or ""
                                if radioId:
                                    try:
                                        label = self.driver.find_element(By.XPATH, f"//label[@for='{radioId}']")
                                        labelText = label.text.lower()
                                        if "sim" in labelText or "yes" in labelText:
                                            radio.click()
                                            time.sleep(0.3)
                                    except:
                                        pass
                        except:
                            pass
                except:
                    pass
            
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"  ⚠️ Erro ao responder perguntas: {str(e)[:100]}")



    def submitFinalApplication(self):
        """
        Envia a candidatura final
        """
        try:
            # Procurar botão de enviar final
            submitTexts = [
                "Enviar candidatura",
                "Submit application",
                "Enviar",
                "Submit",
                "Candidatar"
            ]
            
            for submitText in submitTexts:
                try:
                    buttons = self.driver.find_elements(By.XPATH, f"//button[contains(., '{submitText}') or contains(@aria-label, '{submitText}')]")
                    for btn in buttons:
                        if btn.is_displayed() and btn.is_enabled():
                            utils.prGreen(f"  📤 Enviando candidatura...")
                            try:
                                btn.click()
                            except:
                                self.driver.execute_script("arguments[0].click();", btn)
                            
                            time.sleep(random.uniform(2, 3))
                            utils.prGreen("  ✅ Candidatura enviada!")
                            return "applied"
                except:
                    pass
            
            return "failed"
            
        except:
            return "failed"

    
    def displayWriteResults(self, lineToWrite: str):
        """
        Exibe e salva os resultados em arquivo
        """
        try:
            print(lineToWrite)
            utils.writeResults(lineToWrite)
        except Exception as e:
            if config.displayWarnings:
                utils.prRed(f"❌ Erro ao salvar resultados: {str(e)}")


# ============================================
# EXECUÇÃO DO BOT
# ============================================

if __name__ == "__main__":
    try:
        start_time = time.time()
        
        # Iniciar bot
        bot = LinkedinBot()
        
        # Calcular tempo de execução
        end_time = time.time()
        elapsed_time = round((end_time - start_time) / 60, 2)
        
        utils.prBlue(f"\n⏱️ Tempo total de execução: {elapsed_time} minuto(s)")
        
    except KeyboardInterrupt:
        utils.prYellow("\n\n⚠️ Bot interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        utils.prRed(f"\n❌ Erro fatal: {str(e)}")
        sys.exit(1)
