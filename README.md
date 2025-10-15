# Bot de Aplicação Automática no LinkedIn

Bot em Python para aplicar automaticamente em vagas do LinkedIn usando o recurso "Easy Apply", com **perfil isolado do Selenium**.

## 🔒 Segurança e Privacidade

Este bot utiliza um **perfil isolado do Selenium** criado na pasta `selenium_profile/` do projeto. Seu perfil pessoal do Chrome **NÃO é afetado**. Na primeira execução, você precisará fazer login no LinkedIn, e esse login ficará salvo no perfil isolado para as próximas execuções.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Conta no LinkedIn com pelo menos um currículo anexado

## 🚀 Instalação

### 1. Clone o projeto

```bash
git clone [seu-repositorio]
cd LinkdinBot
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## ▶️ Como usar

### Opção 1: Interface Gráfica (Recomendado)

Execute a interface gráfica:

```bash
python gui_config.py
```

1. Configure suas preferências nas abas
2. Clique em "Salvar e Executar Bot"
3. Na primeira vez, faça login no LinkedIn quando o Chrome abrir
4. O bot começará a aplicar automaticamente

### Opção 2: Linha de Comando

1. Edite o arquivo `config.py` com suas preferências
2. Execute:

```bash
python linkedin.py
```

## ⚙️ Configurações Importantes

### Busca de Vagas

- **Localização**: Onde procurar vagas (ex: `['Brazil', 'Remote']`)
- **Palavras-chave**: Termos relacionados ao cargo (ex: `['Python', 'Developer']`)
- **Nível de experiência**: Júnior, Pleno, Sênior, etc
- **Tipo de trabalho**: Full-time, Contract, etc
- **Modalidade**: Remote, Hybrid, On-site

### Comportamento do Bot

```python
maxApplications = 50  # Limite de candidaturas (0 = sem limite)
botSpeed = 4          # Segundos entre ações (3-8 recomendado)
headless = False      # True = executar sem abrir janela
```

### Blacklist e Whitelist

```python
blacklistCompanies = ['Empresa A', 'Empresa B']  # Empresas para ignorar
blackListTitles = ['senior', 'sênior']           # Títulos para ignorar
```

## 📊 Resultados

Os resultados são salvos em:
- `data/urlData.txt` - URLs de busca geradas
- `Applied_Jobs_DATA_[TIMESTAMP].txt` - Log de todas as candidaturas

## 🛡️ Segurança e Boas Práticas

- ✅ **Use o perfil isolado**: Não afeta seu Chrome pessoal
- ✅ Não aplique em mais de 200 vagas por dia
- ✅ Use velocidade moderada (3-5 segundos)
- ✅ Revise regularmente as vagas aplicadas
- ✅ Mantenha seu perfil e currículo atualizados
- ✅ Use blacklist para evitar empresas indesejadas

## 📁 Estrutura do Projeto

```
LinkdinBot/
├── linkedin.py          # Script principal do bot
├── config.py           # Configurações
├── gui_config.py       # Interface gráfica
├── utils.py            # Funções auxiliares
├── constants.py        # Constantes
├── requirements.txt    # Dependências
├── selenium_profile/   # Perfil isolado (criado automaticamente)
└── data/              # Dados e logs (criado automaticamente)
```

## ❓ Solução de Problemas

### "Você não está logado no LinkedIn"
- Na primeira execução, faça login quando o Chrome abrir
- O login ficará salvo no perfil `selenium_profile/`
- Se precisar fazer login novamente, delete a pasta `selenium_profile/`

### "Nenhum currículo encontrado"
- Acesse seu perfil no LinkedIn
- Vá em "Configurações" > "Privacidade de dados" > "Informações da candidatura"
- Faça upload de pelo menos um currículo

### Bot não encontra vagas
- Verifique se as palavras-chave estão corretas
- Tente localizações mais amplas (ex: "Brazil" ao invés de cidade específica)
- Verifique se os filtros não estão muito restritivos

### Erro ao inicializar Chrome
- Certifique-se que o Google Chrome está instalado
- Tente deletar a pasta `selenium_profile/` e execute novamente

## 🆕 O que mudou nesta versão

✅ **Perfil isolado**: Não usa mais o perfil pessoal do Chrome  
✅ **Métodos corrigidos**: Todos os métodos faltantes foram implementados  
✅ **Tratamento de erros**: Sistema robusto de try/catch  
✅ **GUI simplificada**: Removida aba desnecessária de configuração do Chrome  
✅ **Estatísticas**: Resumo completo ao final da execução  
✅ **Logs melhorados**: Mensagens mais claras e informativas  

## 📝 Licença

Projeto para uso pessoal e educacional.

## ⚠️ Aviso Legal

Este bot é fornecido "como está". Use por sua conta e risco. O autor não se responsabiliza por banimentos ou problemas com sua conta do LinkedIn. Use com moderação e responsabilidade.




