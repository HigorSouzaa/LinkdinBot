# Bot de Aplicação Automática no LinkedIn - Versão Sem Login

Bot em Python para aplicar automaticamente em vagas do LinkedIn usando o recurso "Easy Apply", **sem necessidade de inserir credenciais no código**.

## 🔒 Segurança

Este bot utiliza o **perfil do seu navegador** para manter a sessão logada, evitando que você precise inserir email e senha no código. Isso garante mais segurança e praticidade.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome ou Mozilla Firefox instalado
- Conta no LinkedIn com pelo menos um currículo anexado

## 🚀 Instalação

### 1. Clone ou baixe o projeto

git clone [seu-repositorio]
cd linkedin-bot


### 2. Instale as dependências

pip install -r requirements.txt


### 3. Configure o perfil do navegador

#### Para Chrome:

1. Abra o Chrome
2. Faça login no LinkedIn normalmente
3. Digite `chrome://version/` na barra de endereços
4. Copie o **Caminho do perfil** (remova o nome do perfil no final, ex: `/Default`)
5. Abra o arquivo `config.py`
6. Cole o caminho em `chromeProfilePath`
7. Configure `chromeProfileName` (geralmente "Default")

Exemplo:

chromeProfilePath = r"C:\Users\SeuNome\AppData\Local\Google\Chrome\User Data"
chromeProfileName = "Default"


#### Para Firefox:

1. Abra o Firefox
2. Faça login no LinkedIn normalmente
3. Digite `about:profiles` na barra de endereços
4. Copie o **Diretório raiz** do perfil ativo
5. Abra o arquivo `config.py`
6. Cole o caminho em `firefoxProfilePath`

### 4. Configure suas preferências

Edite o arquivo `config.py` e ajuste:

- **Localização**: onde procurar vagas
- **Palavras-chave**: termos relacionados ao cargo desejado
- **Nível de experiência**: júnior, pleno, sênior, etc
- **Tipo de trabalho**: remoto, híbrido, presencial
- **Filtros adicionais**: blacklist de empresas/títulos, etc

## ▶️ Como usar

Execute o bot:

python linkedin.py

O bot irá:
1. Abrir o navegador usando seu perfil (já logado)
2. Verificar se está logado no LinkedIn
3. Gerar URLs de busca baseadas em suas configurações
4. Navegar pelas vagas encontradas
5. Aplicar automaticamente nas vagas "Easy Apply"
6. Salvar os resultados na pasta `data/`

## 📊 Resultados

Os resultados são salvos em:
- `data/urlData.txt` - URLs de busca geradas
- `data/Candidaturas_Aplicadas_[DATA].txt` - Log de todas as candidaturas

## ⚙️ Configurações Importantes

### Velocidade do Bot

botSpeed = 4 # Segundos entre ações (recomendado: 3-5)


### Limite de Candidaturas

maxApplications = 50 # 0 = sem limite


### Modo Headless

headless = False # True = executar em background sem abrir janela


## 🛡️ Segurança e Boas Práticas

- ✅ Não aplique em mais de 200 vagas por dia
- ✅ Use velocidade moderada (3-5 segundos)
- ✅ Revise regularmente as vagas aplicadas
- ✅ Mantenha seu perfil e currículo atualizados
- ✅ Use blacklist para evitar empresas indesejadas

## ❓ Solução de Problemas

### "Você não está logado no LinkedIn"
- Certifique-se de que o perfil do navegador está configurado corretamente
- Abra o navegador manualmente com esse perfil e verifique se está logado
- Tente fazer logout e login novamente no LinkedIn

### "Nenhum currículo encontrado"
- Acesse seu perfil no LinkedIn
- Vá em "Configurações" > "Privacidade de dados" > "Informações da candidatura"
- Faça upload de pelo menos um currículo

### Bot não encontra vagas
- Verifique se as palavras-chave estão corretas
- Tente localizações mais amplas (ex: "Brazil" ao invés de cidade específica)
- Verifique se os filtros não estão muito restritivos

## 📝 Licença

Projeto para uso pessoal e educacional.

## ⚠️ Aviso Legal

Este bot é fornecido "como está". Use por sua conta e risco. O autor não se responsabiliza por banimentos ou problemas com sua conta do LinkedIn. Use com moderação e responsabilidade.




