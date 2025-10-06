# config.py - Configurações do Bot de Aplicação Automática no LinkedIn
# Todos os comentários em Português Brasileiro

# ============================================
# CONFIGURAÇÕES DO NAVEGADOR
# ============================================

# Navegador que o bot vai usar - ex: "Chrome" ou "Firefox"
browser = "Chrome"

# Modo headless (executar sem abrir janela do navegador) - True para ativar, False para desativar
headless = False

# IMPORTANTE: Para usar o bot SEM credenciais, você precisa configurar o caminho do perfil do navegador
# Como pegar o caminho do perfil:
# - Chrome: digite chrome://version/ na barra de endereços e copie o "Caminho do perfil"
# - Firefox: digite about:profiles na barra de endereços e copie o "Diretório raiz"

# Caminho do perfil do Chrome (deixe vazio "" se não for usar)
# Exemplo Windows: r"C:\Users\SeuUsuario\AppData\Local\Google\Chrome\User Data"
# Exemplo Linux: r"/home/seuusuario/.config/google-chrome"
chromeProfilePath = r"C:\Users\Hzzin\AppData\Local\Google\Chrome\User Data"

# Nome do perfil do Chrome (geralmente "Default" ou "Profile 1", "Profile 2", etc)
chromeProfileName = "Default"

# Caminho do perfil do Firefox (deixe vazio "" se não for usar)
# Exemplo: r"C:\Users\SeuUsuario\AppData\Roaming\Mozilla\Firefox\Profiles\xxxxxxxx.default-release"
firefoxProfilePath = r""


# ============================================
# CONFIGURAÇÕES DE BUSCA DE VAGAS
# ============================================

# Localizações onde buscar vagas
# Exemplos: ["Brazil"], ["United States"], ["Remote"], ["São Paulo, Brazil"]
# Continentes: ["Europe", "Asia", "Australia", "NorthAmerica", "SouthAmerica", "Africa"]
location = ["Brazil", "Remote"]

# Palavras-chave relacionadas às vagas que você procura
keywords = ["frontend", "react", "typescript", "javascript", "desenvolvedor", "developer"]

# Nível de experiência desejado
# Opções: "Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive"
experienceLevels = ["Entry level", "Associate"]

# Data de postagem da vaga
# Opções: "Any Time", "Past Month", "Past Week", "Past 24 hours" - escolha apenas UMA
datePosted = ["Past Week"]

# Tipo de trabalho
# Opções: "Full-time", "Part-time", "Contract", "Temporary", "Volunteer", "Internship", "Other"
jobType = ["Full-time", "Contract"]

# Modalidade de trabalho
# Opções: "On-site", "Remote", "Hybrid"
remote = ["Remote", "Hybrid"]

# Faixa salarial mínima (em dólares)
# Opções: "$40,000+", "$60,000+", "$80,000+", "$100,000+", "$120,000+", "$140,000+", 
#         "$160,000+", "$180,000+", "$200,000+" - escolha apenas UMA
# Deixe vazio [""] para não filtrar por salário
salary = [""]

# Ordenação dos resultados
# Opções: "Recent" (mais recentes) ou "Relevant" (mais relevantes) - escolha apenas UMA
sort = ["Recent"]


# ============================================
# FILTROS AVANÇADOS (BLACKLIST/WHITELIST)
# ============================================

# Empresas que você NÃO quer se candidatar (blacklist)
# Exemplo: ["Apple", "Google", "Amazon"]
blacklistCompanies = []

# Palavras-chave em títulos que você quer EVITAR
# Exemplo: ["senior", "manager", "lead", ".Net"]
blackListTitles = ["senior", "sênior", "pleno"]

# Apenas se candidatar nessas empresas específicas (deixe vazio [] para todas)
# Exemplo: ["Microsoft", "Meta", "Netflix"]
onlyApplyCompanies = []

# Apenas se candidatar em vagas com essas palavras no título (deixe vazio [] para todas)
# Exemplo: ["junior", "react", "frontend"]
onlyApplyTitles = []


# ============================================
# CONFIGURAÇÕES DE APLICAÇÃO
# ============================================

# Seguir empresas após candidatura bem-sucedida? True = sim, False = não
followCompanies = False

# Qual currículo usar (se tiver vários no LinkedIn)
# 1 = primeiro da lista, 2 = segundo, etc
preferredCv = 1

# Salvar a vaga antes de aplicar? True = sim, False = não
saveBeforeApply = False

# Número máximo de candidaturas por execução (0 = sem limite)
maxApplications = 0


# ============================================
# CONFIGURAÇÕES DE SAÍDA/LOGS
# ============================================

# Mostrar avisos detalhados durante execução? True = sim, False = não
displayWarnings = True

# Tipo de arquivo de saída para resultados
# Opções: ".txt" ou ".csv"
outputFileType = ".txt"


# ============================================
# CONFIGURAÇÕES DE VELOCIDADE
# ============================================

# Velocidade do bot (em segundos entre ações)
# Valores recomendados: 2-3 (rápido), 3-5 (médio), 5-8 (lento/seguro)
botSpeed = 4
