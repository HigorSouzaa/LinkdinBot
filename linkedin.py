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
            time.sleep(3)
            
            # Tentar encontrar elementos que só aparecem quando logado
            try:
                # Procurar pela barra de navegação do feed
                self.driver.find_element(By.XPATH, "//nav[contains(@class, 'global-nav')]")
                return True
            except:
                pass
            
            # Verificar se está na página de login
            current_url = self.driver.current_url
            if "login" in current_url or "authwall" in current_url:
                return False
            
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
        
        # Obter título da vaga
        try:
            jobTitleElement = self.driver.find_element(By.XPATH, "//h1[contains(@class, 'job') or contains(@class, 'title')]")
            jobTitle = jobTitleElement.text.strip()
            
            # Verificar blacklist de títulos
            for blacklistedTitle in config.blackListTitles:
                if blacklistedTitle.lower() in jobTitle.lower():
                    jobTitle += f" (BLACKLISTED: {blacklistedTitle})"
                    break
        except:
            jobTitle = "Título não encontrado"
        
        # Obter detalhes da vaga (empresa, localização, etc)
        try:
            time.sleep(1)
            jobDetailsElement = self.driver.find_element(By.XPATH, "//div[contains(@class, 'job-details')]")
            jobDetails = jobDetailsElement.text.replace("\n", " | ")
            
            # Verificar blacklist de empresas
            for blacklistedCompany in config.blacklistCompanies:
                if blacklistedCompany.lower() in jobDetails.lower():
                    jobDetails += f" (BLACKLISTED COMPANY: {blacklistedCompany})"
                    break
        except:
            jobDetails = "Detalhes não encontrados"
        
        # Obter informações de modalidade (remoto, híbrido, presencial)
        try:
            workModeElements = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'ui-label')]")
            for element in workModeElements:
                jobLocation += " | " + element.text
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
            # Verificar se o botão Easy Apply existe
            easyApplyButton = self.findEasyApplyButton()
            
            if easyApplyButton is None:
                return "failed"
            
            if easyApplyButton == "already_applied":
                return "already_applied"
            
            # Clicar no botão Easy Apply
            easyApplyButton.click()
            time.sleep(random.uniform(1, config.botSpeed))
            
            # Salvar vaga antes de aplicar (se configurado)
            if config.saveBeforeApply:
                try:
                    saveButton = self.driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Save')]")
                    if "saved" not in saveButton.get_attribute("aria-label").lower():
                        saveButton.click()
                        time.sleep(0.5)
                except:
                    pass
            
            # Tentar aplicação simples (sem etapas adicionais)
            try:
                self.chooseResume()
                submitButton = self.driver.find_element(By.CSS_SELECTOR, constants.submitButtonSelector)
                submitButton.click()
                time.sleep(random.uniform(1, config.botSpeed))
                return "applied"
            
            except:
                # Aplicação com múltiplas etapas
                try:
                    return self.applyMultiStep(offerPage)
                except:
                    return "failed"
        
        except Exception as e:
            if config.displayWarnings:
                utils.prYellow(f"  ⚠️ Erro ao aplicar: {str(e)}")
            return "failed"
    
    def findEasyApplyButton(self):
        """
        Procura o botão Easy Apply na página
        Retorna o elemento do botão, 'already_applied', ou None
        """
        try:
            time.sleep(random.uniform(1, 2))
            
            # Verificar se já aplicou
            try:
                appliedText = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Applied') or contains(text(), 'Candidatou-se')]")
                if appliedText:
                    return "already_applied"
            except:
                pass
            
            # Procurar botão Easy Apply
            try:
                button = self.driver.find_element(By.XPATH, constants.easyApplyButtonXPath)
                return button
            except:
                pass
            
            # Tentar outro seletor
            try:
                button = self.driver.find_element(By.XPATH, "//button[contains(., 'Easy Apply') or contains(., 'Candidatura simples')]")
                return button
            except:
                pass
            
            return None
            
        except:
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
