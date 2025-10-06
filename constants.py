# constants.py - Constantes utilizadas pelo bot
# Valores fixos que não devem ser alterados

# ============================================
# URLS E ENDPOINTS
# ============================================

# URL base para busca de vagas no LinkedIn
linkJobUrl = "https://www.linkedin.com/jobs/search/"

# URL da página de jobs
jobsPageUrl = "https://www.linkedin.com/jobs"

# URL do feed do LinkedIn (usado para verificar se está logado)
linkedinFeedUrl = "https://www.linkedin.com/feed"


# ============================================
# CONFIGURAÇÕES DE PAGINAÇÃO
# ============================================

# Número de vagas exibidas por página no LinkedIn
jobsPerPage = 25

# Número máximo de páginas a processar por busca (LinkedIn limita em ~40 páginas)
maxPages = 40


# ============================================
# SELETORES XPATH E CSS
# ============================================

# XPath para encontrar o total de vagas
totalJobsSelector = "//small"

# XPath para encontrar cada card de vaga na lista
offersPerPageSelector = "//li[@data-occludable-job-id]"

# XPath para o botão Easy Apply
easyApplyButtonXPath = '//button[contains(@class, "jobs-apply-button")]'

# CSS Selector para botão de continuar
continueButtonSelector = "button[aria-label='Continue to next step']"

# CSS Selector para botão de revisar candidatura
reviewButtonSelector = "button[aria-label='Review your application']"

# CSS Selector para botão de enviar candidatura
submitButtonSelector = "button[aria-label='Submit application']"

# CSS Selector para checkbox de seguir empresa
followCompanyCheckboxSelector = "label[for='follow-company-checkbox']"


# ============================================
# MENSAGENS E TEXTOS
# ============================================

# Nome do projeto
projectName = "LinkedIn Easy Apply Bot - Versão Sem Login"

# Versão
version = "1.0.0"

# Texto de boas-vindas
welcomeMessage = "🤖 Bot de Aplicação Automática no LinkedIn iniciando..."

# Texto de conclusão
doneMessage = "✅ Processo de candidaturas concluído!"
