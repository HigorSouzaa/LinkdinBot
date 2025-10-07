# linkedin.py - Script principal do bot de aplicação no LinkedIn
# Este é o arquivo principal que você vai executar

import time
import math
import random
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

# Importar módulos do projeto
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
        """
        Gera as URLs de busca baseadas nas configurações
        e salva em um arquivo data/urlData.txt
        """
        utils.prYellow("🔗 Gerando URLs de busca...")
        
        # Criar pasta data se não existir
        if not os.path.exists('data'):
            os.makedirs('data')
            utils.prGreen("✅ Pasta 'data' criada")
        
        try:
            urls = utils.LinkedinUrlGenerate().generateUrlLinks()
            
            with open('data/urlData.txt', 'w', encoding='utf-8') as file:
                for url in urls:
                    file.write(url + "\n")
            
            utils.prGreen(f"✅ {len(urls)} URLs de busca criadas com sucesso!")
            utils.prYellow(f"📊 Combinações: {len(config.location)} localizações × {len(config.keywords)} palavras-chave")
            
        except Exception as e:
            utils.prRed(f"❌ Erro ao gerar URLs: {str(e)}")
            utils.prRed("❌ Verifique as configurações no config.py (linhas de location e keywords)")
            sys.exit(1)
    
    def startApplying(self):
        """
        Inicia o processo de aplicação nas vagas
        """
        # Gerar URLs de busca
        self.generateUrls()
        
        # Contadores
        countApplied = 0
        countJobs = 0
        countSkipped = 0
        
        # Ler URLs geradas
        urlData = utils.getUrlDataFile()
        
        if not urlData:
            utils.prRed("❌ Nenhuma URL encontrada para processar")
            self.driver.quit()
            sys.exit(1)
        
        utils.prBlue("\n" + "=" * 60)
        utils.prBlue("🚀 INICIANDO PROCESSO DE CANDIDATURAS")
        utils.prBlue("=" * 60 + "\n")
        
        # Processar cada URL de busca
        for urlIndex, url in enumerate(urlData, 1):
            utils.prYellow(f"\n📍 Processando busca {urlIndex}/{len(urlData)}")
            
            try:
                self.driver.get(url)
                time.sleep(random.uniform(2, config.botSpeed))
                
                # Obter número total de vagas
                try:
                    totalJobsElement = self.driver.find_element(By.XPATH, constants.totalJobsSelector)
                    totalJobsText = totalJobsElement.text
                    totalPages = utils.jobsToPages(totalJobsText)
                    
                    utils.prGreen(f"✅ Encontradas {totalJobsText} vagas")
                    utils.prYellow(f"📄 Processando {totalPages} páginas...")
                except:
                    utils.prYellow("⚠️ Não foi possível obter o número total de vagas")
                    totalPages = 1
                
                # Obter palavras-chave da URL
                urlWords = utils.urlToKeywords(url)
                lineToWrite = f"\n Categoria: {urlWords[0]}, Localização: {urlWords[1]}, Total: {totalJobsText if 'totalJobsText' in locals() else 'Desconhecido'}"
                self.displayWriteResults(lineToWrite)
                
                # Processar cada página de resultados
                for page in range(totalPages):
                    currentPageJobs = constants.jobsPerPage * page
                    pageUrl = url + "&start=" + str(currentPageJobs)
                    
                    self.driver.get(pageUrl)
                    time.sleep(random.uniform(1, config.botSpeed))
                    
                    utils.prYellow(f"  📄 Página {page + 1}/{totalPages}")
                    
                    # Obter lista de vagas na página
                    try:
                        offersPerPage = self.driver.find_elements(By.XPATH, constants.offersPerPageSelector)
                        offerIds = []
                        
                        for offer in offersPerPage:
                            offerId = offer.get_attribute("data-occludable-job-id")
                            if offerId:
                                jobId = offerId.split(":")[-1]
                                offerIds.append(jobId)
                        
                        utils.prGreen(f"  ✅ {len(offerIds)} vagas encontradas nesta página")
                        
                    except Exception as e:
                        if config.displayWarnings:
                            utils.prYellow(f"  ⚠️ Erro ao obter vagas da página: {str(e)}")
                        continue
                    
                    # Processar cada vaga
                    for jobId in offerIds:
                        # Verificar limite de candidaturas
                        if config.maxApplications > 0 and countApplied >= config.maxApplications:
                            utils.prYellow(f"\n⚠️ Limite de {config.maxApplications} candidaturas atingido!")
                            break
                        
                        offerPage = f'https://www.linkedin.com/jobs/view/{jobId}'
                        
                        try:
                            self.driver.get(offerPage)
                            time.sleep(random.uniform(1, config.botSpeed))
                            
                            countJobs += 1
                            
                            # Obter informações da vaga
                            jobProperties = self.getJobProperties(countJobs)
                            
                            # Verificar blacklist
                            if "blacklisted" in jobProperties.lower():
                                lineToWrite = f"{jobProperties} | * 🚫 Vaga ignorada (blacklist): {offerPage}"
                                self.displayWriteResults(lineToWrite)
                                countSkipped += 1
                                continue
                            
                            # Verificar whitelist (se configurado)
                            if config.onlyApplyCompanies or config.onlyApplyTitles:
                                if not self.checkWhitelist(jobProperties):
                                    lineToWrite = f"{jobProperties} | * ⏭️ Vaga ignorada (não está na whitelist): {offerPage}"
                                    self.displayWriteResults(lineToWrite)
                                    countSkipped += 1
                                    continue
                            
                            # Tentar aplicar para a vaga
                            result = self.applyToJob(offerPage)
                            
                            if result == "applied":
                                lineToWrite = f"{jobProperties} | * 🥳 Candidatura enviada com sucesso!: {offerPage}"
                                countApplied += 1
                            elif result == "already_applied":
                                lineToWrite = f"{jobProperties} | * ✅ Já aplicado anteriormente: {offerPage}"
                            else:
                                lineToWrite = f"{jobProperties} | * ⚠️ Não foi possível aplicar: {offerPage}"
                                countSkipped += 1
                            
                            self.displayWriteResults(lineToWrite)
                            
                        except Exception as e:
                            if config.displayWarnings:
                                utils.prRed(f"  ❌ Erro ao processar vaga {jobId}: {str(e)}")
                            countSkipped += 1
                            continue
                    
                    # Verificar se atingiu o limite
                    if config.maxApplications > 0 and countApplied >= config.maxApplications:
                        break
                
                # Resumo da busca atual
                utils.prBlue(f"\n📊 Resumo da busca: {urlWords[0]}, {urlWords[1]}")
                utils.prGreen(f"  ✅ Candidaturas enviadas: {countApplied}")
                utils.prYellow(f"  ⏭️ Vagas ignoradas: {countSkipped}")
                utils.prBlue(f"  📋 Total processado: {countJobs}")
                
            except Exception as e:
                utils.prRed(f"❌ Erro ao processar URL: {str(e)}")
                continue
        
        # Resumo final
        utils.prBlue("\n" + "=" * 60)
        utils.prBlue("📊 RESUMO FINAL")
        utils.prBlue("=" * 60)
        utils.prGreen(f"✅ Total de candidaturas enviadas: {countApplied}")
        utils.prYellow(f"⏭️ Total de vagas ignoradas: {countSkipped}")
        utils.prBlue(f"📋 Total de vagas processadas: {countJobs}")
        utils.prBlue("=" * 60 + "\n")
        
        utils.prGreen(constants.doneMessage)
        
        # Fechar navegador
        time.sleep(3)
        self.driver.quit()

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
        Aplica para vagas com múltiplas etapas
        Retorna 'applied' ou 'failed'
        """
        try:
            # Clicar em continuar
            continueButton = self.driver.find_element(By.CSS_SELECTOR, constants.continueButtonSelector)
            continueButton.click()
            time.sleep(random.uniform(1, config.botSpeed))
            
            self.chooseResume()
            
            # Obter percentual de completude
            try:
                percentageElement = self.driver.find_element(By.XPATH, "//span[contains(text(), '%')]")
                percentageText = percentageElement.text
                percentage = int(percentageText.replace("%", ""))
            except:
                percentage = 0
            
            # Calcular número de páginas
            if percentage > 0:
                applyPages = math.floor(100 / percentage) - 2
            else:
                applyPages = 1
            
            # Navegar pelas páginas
            for _ in range(applyPages):
                try:
                    continueButton = self.driver.find_element(By.CSS_SELECTOR, constants.continueButtonSelector)
                    continueButton.click()
                    time.sleep(random.uniform(1, config.botSpeed))
                except:
                    break
            
            # Revisar aplicação
            try:
                reviewButton = self.driver.find_element(By.CSS_SELECTOR, constants.reviewButtonSelector)
                reviewButton.click()
                time.sleep(random.uniform(1, config.botSpeed))
            except:
                pass
            
            # Desmarcar opção de seguir empresa (se configurado)
            if not config.followCompanies:
                try:
                    followCheckbox = self.driver.find_element(By.CSS_SELECTOR, constants.followCompanyCheckboxSelector)
                    followCheckbox.click()
                    time.sleep(0.5)
                except:
                    pass
            
            # Enviar candidatura
            submitButton = self.driver.find_element(By.CSS_SELECTOR, constants.submitButtonSelector)
            submitButton.click()
            time.sleep(random.uniform(1, config.botSpeed))
            
            return "applied"
            
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"  ⚠️ Erro na aplicação multi-step: {str(e)}")
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
