# config.py - Configurações do Bot (Gerado automaticamente pela GUI)

# ============================================
# CONFIGURAÇÕES DO NAVEGADOR
# ============================================
browser = "Chrome"
headless = False

# Nota: O bot usa perfil isolado na pasta "selenium_profile"
# Na primeira execução, faça login no LinkedIn
# O login ficará salvo automaticamente

# ============================================
# BUSCA DE VAGAS
# ============================================
location = ['Brazil', 'Remote']
keywords = ['React Native', 'React', 'Node.js', 'Express.js', 'Javascript', 'C#', 'backend', 'frontend']

# ============================================
# FILTROS DE BUSCA
# ============================================
experienceLevels = ['Pleno']
datePosted = ["Any Time"]
jobType = ['Full-time', 'Contract']
remote = ['Remote']
salary = [""]
sort = ["Recent"]

# ============================================
# BLACKLIST E WHITELIST
# ============================================
blacklistCompanies = []
blackListTitles = ['senior', 'sênior', 'pleno']
onlyApplyCompanies = []
onlyApplyTitles = []

# ============================================
# COMPORTAMENTO DO BOT
# ============================================
followCompanies = False
preferredCv = 1
saveBeforeApply = False
maxApplications = 10

# ============================================
# CONFIGURAÇÕES TÉCNICAS
# ============================================
displayWarnings = True
outputFileType = ".txt"
botSpeed = 5

# ============================================
# INFORMAÇÕES PESSOAIS (para preenchimento automático)
# ============================================
personalInfo = {
    "yearsOfExperience": "2",
    "salaryExpectation": "3000",
    "phone": "19999737199",
    "city": "São Paulo",
    "country": "Brasil",
    "availability": "imediata",
    "hourlyRate": "50",
    "englishLevel": "básico",
    "otherLanguages": "",
    "acceptRemote": "sim",
    "acceptRelocation": "não",
    "linkedinUrl": "",
    "portfolioUrl": "",
    "additionalNotes": ""
}

# ============================================
# PREENCHIMENTO AUTOMÁTICO DE FORMULÁRIOS
# ============================================
autoFillEnabled = True
autoSelectYes = True
autoSelectFirstOption = True
