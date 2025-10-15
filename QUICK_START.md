# 🚀 Guia de Início Rápido - LinkedIn Bot

## ⚡ Instalação em 3 Passos

### 1️⃣ Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar Interface Gráfica
```bash
python gui_config.py
```

### 3️⃣ Configurar e Executar
1. Preencha as configurações nas 3 abas
2. Clique em "Salvar e Executar Bot"
3. **Faça login no LinkedIn quando o Chrome abrir** (apenas primeira vez)
4. Aguarde o bot processar as vagas

---

## 📋 Configuração Mínima

Se preferir editar o arquivo `config.py` diretamente:

```python
# OBRIGATÓRIO: Configure estas 2 linhas
location = ['Brazil', 'Remote']  # Onde procurar
keywords = ['Python', 'Developer']  # O que procurar

# RECOMENDADO: Configure seu nível
experienceLevels = ['Júnior']  # Ou 'Pleno', 'Sênior'

# OPCIONAL: Limite de candidaturas
maxApplications = 10  # 0 = sem limite
```

Depois execute:
```bash
python linkedin.py
```

---

## 🎯 Primeira Execução

**IMPORTANTE**: Na primeira vez que executar o bot:

1. ✅ O Chrome abrirá automaticamente
2. ✅ Você verá uma página do LinkedIn
3. ⚠️ **VOCÊ PRECISA FAZER LOGIN MANUALMENTE**
4. ✅ Após fazer login, o bot continuará automaticamente
5. ✅ **O login ficará salvo** - não precisa fazer de novo

**Onde fica salvo?** Na pasta `selenium_profile/` do projeto

---

## 🔄 Execuções Seguintes

Nas próximas vezes:
- ✅ Já vai estar logado automaticamente
- ✅ O bot começa a trabalhar direto
- ✅ Não precisa fazer nada manualmente

---

## 📊 O que o Bot Faz

1. Abre o Chrome com perfil isolado
2. Acessa o LinkedIn (já logado)
3. Busca vagas baseado nas suas configurações
4. Aplica automaticamente usando "Easy Apply"
5. Preenche formulários com suas informações
6. Mostra estatísticas ao final

---

## ⚙️ Configurações Importantes

### Velocidade
```python
botSpeed = 5  # Segundos entre ações (3-8 recomendado)
```
- **Muito rápido** (2-3s): Risco de ser detectado
- **Ideal** (4-6s): Mais seguro
- **Muito lento** (8+s): Demorado mas seguro

### Limite Diário
```python
maxApplications = 50  # Limite por execução
```
- **Recomendado**: Máximo 200 por dia
- **Seguro**: 50-100 por execução
- **0**: Sem limite (use com cuidado!)

### Blacklist (Ignorar)
```python
blackListTitles = ['senior', 'sênior', 'pleno']
blacklistCompanies = ['Empresa Ruim']
```

---

## 🐛 Problemas Comuns

### "Você não está logado"
**Solução**: Delete a pasta `selenium_profile/` e execute novamente

### "Nenhum currículo encontrado"
**Solução**: 
1. Acesse linkedin.com
2. Vá em Configurações → Privacidade de dados
3. Faça upload de um currículo

### Bot não encontra vagas
**Solução**:
- Use palavras-chave mais genéricas
- Experimente localizações amplas ('Brazil' ao invés de 'São Paulo')
- Reduza filtros (aceite mais tipos de trabalho)

### Erro ao abrir Chrome
**Solução**:
1. Certifique-se que o Chrome está instalado
2. Delete a pasta `selenium_profile/`
3. Execute novamente

---

## 📞 Ajuda Adicional

- 📖 Leia o `README.md` completo
- 📝 Veja o `CHANGELOG.md` para novidades
- 🔍 Verifique os comentários no `config.py`

---

## 🎉 Pronto!

Agora é só executar e deixar o bot trabalhar para você! 🤖

**Dica**: Comece com `maxApplications = 10` para testar, depois aumente gradualmente.
