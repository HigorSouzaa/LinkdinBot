# gui_config.py - Interface Gráfica COMPLETA do LinkedIn Bot
# Versão 2.0 - Com logs em tempo real e controle total
# -*- coding: utf-8 -*-
import sys
import os

# Forçar UTF-8 antes de qualquer coisa
if sys.platform == "win32":
    try:
        os.system("chcp 65001 > nul")
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass



import customtkinter as ctk
from tkinter import messagebox, filedialog, scrolledtext
import threading
import subprocess
import sys
import os
import time
import re

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LinkedInBotGUI:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("LinkedIn Easy Apply Bot - Configurador v2.0")
        self.window.geometry("950x750")
        
        # Centralizar a janela
        self.center_window(950, 750)
        
        # Carregar configurações existentes
        self.config = self.load_config()
        
        # Variável para controlar processo do bot
        self.bot_process = None
        self.is_running = False
        
        # Criar interface
        self.create_widgets()
        
    def center_window(self, width, height):
        """Centraliza a janela na tela"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.window.geometry(f"{width}x{height}+{x}+{y}")
    
    def load_config(self):
        """Carrega configurações do config.py"""
        default_config = {
            "browser": "Chrome",
            "headless": False,
            "location": ["Brazil"],
            "keywords": ["desenvolvedor"],
            "experienceLevels": ["Júnior"],
            "datePosted": ["Past Week"],
            "jobType": ["Full-time"],
            "remote": ["Remote"],
            "blacklistCompanies": [],
            "blackListTitles": [],
            "followCompanies": False,
            "maxApplications": 0,
            "botSpeed": 4,
            "personalInfo": {
                "yearsOfExperience": "2",
                "salaryExpectation": "3500",
                "phone": "11999999999",
                "city": "São Paulo",
                "country": "Brasil",
                "availability": "imediata",
                "englishLevel": "intermediário"
            }
        }
        
        try:
            import config as cfg
            loaded_config = {
                "browser": getattr(cfg, 'browser', 'Chrome'),
                "headless": getattr(cfg, 'headless', False),
                "location": getattr(cfg, 'location', ["Brazil"]),
                "keywords": getattr(cfg, 'keywords', ["desenvolvedor"]),
                "experienceLevels": getattr(cfg, 'experienceLevels', ["Júnior"]),
                "datePosted": getattr(cfg, 'datePosted', ["Past Week"]),
                "jobType": getattr(cfg, 'jobType', ["Full-time"]),
                "remote": getattr(cfg, 'remote', ["Remote"]),
                "blacklistCompanies": getattr(cfg, 'blacklistCompanies', []),
                "blackListTitles": getattr(cfg, 'blackListTitles', []),
                "followCompanies": getattr(cfg, 'followCompanies', False),
                "maxApplications": getattr(cfg, 'maxApplications', 0),
                "botSpeed": getattr(cfg, 'botSpeed', 4),
                "personalInfo": getattr(cfg, 'personalInfo', default_config["personalInfo"])
            }
            return loaded_config
        except:
            return default_config
    
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        
        # Título principal
        title_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        title_frame.pack(pady=15)
        
        title = ctk.CTkLabel(
            title_frame,
            text="⚙️ Configurador do LinkedIn Bot",
            font=("Arial Bold", 26)
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Configure todas as opções antes de iniciar",
            font=("Arial", 12),
            text_color="gray"
        )
        subtitle.pack()
        
        # Criar notebook (abas)
        self.tabview = ctk.CTkTabview(self.window, width=900, height=520)
        self.tabview.pack(pady=10, padx=20)
        
        # Criar abas
        self.tabview.add("🔍 Busca de Vagas")
        self.tabview.add("👤 Informações Pessoais")
        self.tabview.add("⚙️ Avançado")
        
        # Preencher cada aba
        self.create_search_tab()
        self.create_personal_tab()
        self.create_advanced_tab()
        
        # Botões de ação
        button_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        button_frame.pack(pady=15)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Salvar Configurações",
            command=self.save_config_only,
            width=220,
            height=45,
            font=("Arial Bold", 14),
            corner_radius=8
        )
        save_btn.pack(side="left", padx=10)
        
        run_btn = ctk.CTkButton(
            button_frame,
            text="▶️ Salvar e Executar Bot",
            command=self.save_and_run,
            width=220,
            height=45,
            font=("Arial Bold", 14),
            fg_color="#2E7D32",
            hover_color="#1B5E20",
            corner_radius=8
        )
        run_btn.pack(side="left", padx=10)
    
    def create_search_tab(self):
        """Cria aba de busca de vagas"""
        tab = self.tabview.tab("🔍 Busca de Vagas")
        
        scroll_frame = ctk.CTkScrollableFrame(tab, width=850, height=420)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Palavras-chave
        ctk.CTkLabel(scroll_frame, text="Palavras-chave (separe por vírgula):", 
                    font=("Arial Bold", 13)).pack(anchor="w", pady=(10, 5))
        self.keywords_entry = ctk.CTkEntry(scroll_frame, width=750, height=38)
        self.keywords_entry.insert(0, ", ".join(self.config["keywords"]))
        self.keywords_entry.pack(pady=5)
        
        # Localizações
        ctk.CTkLabel(scroll_frame, text="Localizações (separe por vírgula):", 
                    font=("Arial Bold", 13)).pack(anchor="w", pady=(10, 5))
        self.location_entry = ctk.CTkEntry(scroll_frame, width=750, height=38)
        self.location_entry.insert(0, ", ".join(self.config["location"]))
        self.location_entry.pack(pady=5)
        
        # Nível de experiência
        ctk.CTkLabel(scroll_frame, text="Nível de Experiência:", 
                    font=("Arial Bold", 13)).pack(anchor="w", pady=(15, 5))
        
        exp_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        exp_frame.pack(fill="x", pady=5)
        
        self.exp_vars = {}
        exp_levels = ["Estágio", "Júnior", "Pleno", "Sênior", "Diretor", "Executivo"]
        
        for i, level in enumerate(exp_levels):
            var = ctk.BooleanVar(value=level in self.config["experienceLevels"])
            self.exp_vars[level] = var
            cb = ctk.CTkCheckBox(exp_frame, text=level, variable=var, font=("Arial", 12))
            cb.grid(row=i//3, column=i%3, padx=20, pady=5, sticky="w")
        
        # Data de postagem
        ctk.CTkLabel(scroll_frame, text="Data de Postagem:", 
                    font=("Arial Bold", 13)).pack(anchor="w", pady=(15, 5))
        
        self.date_var = ctk.StringVar(value=self.config["datePosted"][0] if self.config["datePosted"] else "Past Week")
        date_options = ["Past 24 hours", "Past Week", "Past Month", "Any Time"]
        
        for option in date_options:
            ctk.CTkRadioButton(scroll_frame, text=option, variable=self.date_var, 
                             value=option, font=("Arial", 12)).pack(anchor="w", padx=20)
        
        # Tipo de trabalho
        ctk.CTkLabel(scroll_frame, text="Tipo de Trabalho:", 
                    font=("Arial Bold", 13)).pack(anchor="w", pady=(15, 5))
        
        job_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        job_frame.pack(fill="x", pady=5)
        
        self.job_type_vars = {}
        job_types = ["Full-time", "Part-time", "Contract", "Internship"]
        
        for i, jtype in enumerate(job_types):
            var = ctk.BooleanVar(value=jtype in self.config["jobType"])
            self.job_type_vars[jtype] = var
            cb = ctk.CTkCheckBox(job_frame, text=jtype, variable=var, font=("Arial", 12))
            cb.grid(row=i//2, column=i%2, padx=20, pady=5, sticky="w")
        
        # Modalidade
        ctk.CTkLabel(scroll_frame, text="Modalidade de Trabalho:", 
                    font=("Arial Bold", 13)).pack(anchor="w", pady=(15, 5))
        
        remote_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        remote_frame.pack(fill="x", pady=5)
        
        self.remote_vars = {}
        remote_types = ["Remote", "Hybrid", "On-site"]
        
        for i, rtype in enumerate(remote_types):
            var = ctk.BooleanVar(value=rtype in self.config["remote"])
            self.remote_vars[rtype] = var
            cb = ctk.CTkCheckBox(remote_frame, text=rtype, variable=var, font=("Arial", 12))
            cb.grid(row=0, column=i, padx=20, pady=5, sticky="w")
    
    def create_personal_tab(self):
        """Cria aba de informações pessoais"""
        tab = self.tabview.tab("👤 Informações Pessoais")
        
        scroll_frame = ctk.CTkScrollableFrame(tab, width=850, height=420)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        personal = self.config["personalInfo"]
        
        # Grid layout para campos
        fields = [
            ("Anos de Experiência:", "exp_years_entry", personal.get("yearsOfExperience", "2"), 300),
            ("Telefone (com DDD):", "phone_entry", personal.get("phone", "11999999999"), 300),
            ("Cidade:", "city_entry", personal.get("city", "São Paulo"), 300),
            ("Expectativa Salarial (R$):", "salary_entry", personal.get("salaryExpectation", "3500"), 300),
        ]
        
        for label_text, attr_name, value, width in fields:
            ctk.CTkLabel(scroll_frame, text=label_text, 
                        font=("Arial Bold", 12)).pack(anchor="w", pady=(12, 5))
            entry = ctk.CTkEntry(scroll_frame, width=width, height=38)
            entry.insert(0, value)
            entry.pack(pady=5, anchor="w")
            setattr(self, attr_name, entry)
        
        # Disponibilidade
        ctk.CTkLabel(scroll_frame, text="Disponibilidade:", 
                    font=("Arial Bold", 12)).pack(anchor="w", pady=(12, 5))
        self.availability_var = ctk.StringVar(value=personal.get("availability", "imediata"))
        availability_options = ["imediata", "15 dias", "30 dias", "45 dias", "60 dias"]
        availability_menu = ctk.CTkOptionMenu(scroll_frame, variable=self.availability_var, 
                                              values=availability_options, width=300, height=38)
        availability_menu.pack(pady=5, anchor="w")
        
        # Nível de inglês
        ctk.CTkLabel(scroll_frame, text="Nível de Inglês:", 
                    font=("Arial Bold", 12)).pack(anchor="w", pady=(12, 5))
        self.english_var = ctk.StringVar(value=personal.get("englishLevel", "intermediário"))
        english_options = ["básico", "intermediário", "avançado", "fluente", "nativo"]
        english_menu = ctk.CTkOptionMenu(scroll_frame, variable=self.english_var, 
                                         values=english_options, width=300, height=38)
        english_menu.pack(pady=5, anchor="w")
    
    def create_advanced_tab(self):
        """Cria aba de configurações avançadas"""
        tab = self.tabview.tab("⚙️ Avançado")
        
        scroll_frame = ctk.CTkScrollableFrame(tab, width=850, height=420)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Limite de candidaturas
        ctk.CTkLabel(scroll_frame, text="Limite de Candidaturas (0 = sem limite):", 
                    font=("Arial Bold", 12)).pack(anchor="w", pady=(10, 5))
        self.max_apps_entry = ctk.CTkEntry(scroll_frame, width=200, height=38)
        self.max_apps_entry.insert(0, str(self.config["maxApplications"]))
        self.max_apps_entry.pack(pady=5, anchor="w")
        
        # Velocidade do bot
        ctk.CTkLabel(scroll_frame, text="Velocidade do Bot (segundos entre ações):", 
                    font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5))
        self.speed_slider = ctk.CTkSlider(scroll_frame, from_=2, to=8, number_of_steps=6, width=450)
        self.speed_slider.set(self.config["botSpeed"])
        self.speed_slider.pack(pady=5, anchor="w")
        self.speed_label = ctk.CTkLabel(scroll_frame, text=f"Atual: {self.config['botSpeed']}s", 
                                       font=("Arial", 11))
        self.speed_label.pack(anchor="w")
        
        def update_speed_label(value):
            self.speed_label.configure(text=f"Atual: {int(value)}s")
        self.speed_slider.configure(command=update_speed_label)
        
        # Blacklist empresas
        ctk.CTkLabel(scroll_frame, text="Empresas para Ignorar (blacklist, separe por vírgula):", 
                    font=("Arial Bold", 12)).pack(anchor="w", pady=(15, 5))
        self.blacklist_companies_entry = ctk.CTkEntry(scroll_frame, width=700, height=38)
        self.blacklist_companies_entry.insert(0, ", ".join(self.config["blacklistCompanies"]))
        self.blacklist_companies_entry.pack(pady=5, anchor="w")
        
        # Blacklist títulos
        ctk.CTkLabel(scroll_frame, text="Palavras em Títulos para Ignorar (separe por vírgula):", 
                    font=("Arial Bold", 12)).pack(anchor="w", pady=(10, 5))
        self.blacklist_titles_entry = ctk.CTkEntry(scroll_frame, width=700, height=38)
        self.blacklist_titles_entry.insert(0, ", ".join(self.config["blackListTitles"]))
        self.blacklist_titles_entry.pack(pady=5, anchor="w")
        
        # Seguir empresas
        self.follow_var = ctk.BooleanVar(value=self.config["followCompanies"])
        ctk.CTkCheckBox(scroll_frame, text="Seguir empresas após candidatura", 
                       variable=self.follow_var, font=("Arial", 12)).pack(anchor="w", pady=(15, 5))
    
    def validate_config(self):
        """Valida as configurações"""
        if not self.keywords_entry.get().strip():
            messagebox.showerror("Erro", "Você precisa adicionar pelo menos uma palavra-chave!")
            return False
        
        if not self.location_entry.get().strip():
            messagebox.showerror("Erro", "Você precisa adicionar pelo menos uma localização!")
            return False
        
        if not any(var.get() for var in self.exp_vars.values()):
            messagebox.showerror("Erro", "Selecione pelo menos um nível de experiência!")
            return False
        
        phone = self.phone_entry.get().strip()
        if not phone or not phone.isdigit() or len(phone) < 10:
            messagebox.showerror("Erro", "Telefone inválido! Use apenas números com DDD (ex: 11999999999)")
            return False
        
        if not self.city_entry.get().strip():
            messagebox.showerror("Erro", "Você precisa informar a cidade!")
            return False
        
        return True
    
    def save_config_only(self):
        """Apenas salva as configurações sem executar"""
        if self.generate_config():
            messagebox.showinfo("Sucesso", "✅ Configurações salvas com sucesso em config.py!")
    
    def generate_config(self):
        """Gera o arquivo config.py"""
        if not self.validate_config():
            return False
        
        keywords = [k.strip() for k in self.keywords_entry.get().split(",") if k.strip()]
        locations = [l.strip() for l in self.location_entry.get().split(",") if l.strip()]
        exp_levels = [level for level, var in self.exp_vars.items() if var.get()]
        job_types = [jtype for jtype, var in self.job_type_vars.items() if var.get()]
        remote_types = [rtype for rtype, var in self.remote_vars.items() if var.get()]
        
        blacklist_companies = [c.strip() for c in self.blacklist_companies_entry.get().split(",") if c.strip()]
        blacklist_titles = [t.strip() for t in self.blacklist_titles_entry.get().split(",") if t.strip()]
        
        config_content = f'''# config.py - Configurações do Bot (Gerado automaticamente pela GUI)

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
location = {locations}
keywords = {keywords}

# ============================================
# FILTROS DE BUSCA
# ============================================
experienceLevels = {exp_levels}
datePosted = ["{self.date_var.get()}"]
jobType = {job_types}
remote = {remote_types}
salary = [""]
sort = ["Recent"]

# ============================================
# BLACKLIST E WHITELIST
# ============================================
blacklistCompanies = {blacklist_companies}
blackListTitles = {blacklist_titles}
onlyApplyCompanies = []
onlyApplyTitles = []

# ============================================
# COMPORTAMENTO DO BOT
# ============================================
followCompanies = {self.follow_var.get()}
preferredCv = 1
saveBeforeApply = False
maxApplications = {int(self.max_apps_entry.get())}

# ============================================
# CONFIGURAÇÕES TÉCNICAS
# ============================================
displayWarnings = True
outputFileType = ".txt"
botSpeed = {int(self.speed_slider.get())}

# ============================================
# INFORMAÇÕES PESSOAIS (para preenchimento automático)
# ============================================
personalInfo = {{
    "yearsOfExperience": "{self.exp_years_entry.get()}",
    "salaryExpectation": "{self.salary_entry.get()}",
    "phone": "{self.phone_entry.get()}",
    "city": "{self.city_entry.get()}",
    "country": "Brasil",
    "availability": "{self.availability_var.get()}",
    "hourlyRate": "50",
    "englishLevel": "{self.english_var.get()}",
    "otherLanguages": "",
    "acceptRemote": "sim",
    "acceptRelocation": "não",
    "linkedinUrl": "",
    "portfolioUrl": "",
    "additionalNotes": ""
}}

# ============================================
# PREENCHIMENTO AUTOMÁTICO DE FORMULÁRIOS
# ============================================
autoFillEnabled = True
autoSelectYes = True
autoSelectFirstOption = True
'''
        
        try:
            with open("config.py", "w", encoding="utf-8") as f:
                f.write(config_content)
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
            return False
    
    def save_and_run(self):
        """Salva configurações e abre janela de execução"""
        if not self.generate_config():
            return
        
        # Abrir janela de execução
        self.window.withdraw()  # Esconder janela principal
        self.open_execution_window()
    
    def open_execution_window(self):
        """Abre janela de execução com logs em tempo real"""
        exec_window = ctk.CTkToplevel(self.window)
        exec_window.title("LinkedIn Bot - Executando")
        exec_window.geometry("900x600")
        
        # Centralizar
        screen_width = exec_window.winfo_screenwidth()
        screen_height = exec_window.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 600) // 2
        exec_window.geometry(f"900x600+{x}+{y}")
        
        # Prevenir fechar sem confirmar
        exec_window.protocol("WM_DELETE_WINDOW", lambda: self.on_closing_execution(exec_window))
        
        # Título
        title = ctk.CTkLabel(exec_window, text="🤖 LinkedIn Bot Executando", font=("Arial Bold", 22))
        title.pack(pady=15)
        
        # Frame de status
        status_frame = ctk.CTkFrame(exec_window, height=80)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(status_frame, text="▶️ Iniciando bot...", 
                                        font=("Arial Bold", 14), text_color="#4CAF50")
        self.status_label.pack(pady=10)
        
        self.stats_label = ctk.CTkLabel(status_frame, text="Vagas aplicadas: 0 | Erros: 0", 
                                       font=("Arial", 12))
        self.stats_label.pack()
        
        # Área de logs
        log_label = ctk.CTkLabel(exec_window, text="📋 Logs em Tempo Real:", 
                                font=("Arial Bold", 13))
        log_label.pack(anchor="w", padx=25, pady=(10, 5))
        
        # Text widget para logs (usando tkinter nativo para ScrolledText)
        import tkinter as tk
        self.log_text = scrolledtext.ScrolledText(
            exec_window,
            wrap=tk.WORD,
            width=100,
            height=18,
            font=("Consolas", 9),
            bg="#1E1E1E",
            fg="#FFFFFF",
            insertbackground="white"
        )
        self.log_text.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Botão de cancelar
        self.cancel_btn = ctk.CTkButton(
            exec_window,
            text="⏹️ Parar Bot",
            command=lambda: self.stop_bot(exec_window),
            width=200,
            height=45,
            font=("Arial Bold", 14),
            fg_color="#D32F2F",
            hover_color="#B71C1C"
        )
        self.cancel_btn.pack(pady=15)
        
        # Executar bot em thread separada
        self.is_running = True
        bot_thread = threading.Thread(target=self.run_bot, args=(exec_window,), daemon=True)
        bot_thread.start()
    
    def run_bot(self, exec_window):
        """Executa o bot em thread separada"""
        try:
            self.log_text.insert("end", "🚀 Iniciando LinkedIn Easy Apply Bot...\n\n")
            self.log_text.see("end")
            exec_window.update()  # Forçar atualização da GUI
            
            # Executar linkedin.py com encoding UTF-8
            import locale
            import subprocess
            
            # Configurar encoding
            env = os.environ.copy()
            env['PYTHONIOENCODING'] = 'utf-8'
            env['PYTHONUNBUFFERED'] = '1'  # Desabilitar buffer para output imediato
            
            self.bot_process = subprocess.Popen(
                [sys.executable, "-u", "linkedin.py"],  # -u para unbuffered
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=0,  # Sem buffer
                universal_newlines=True,
                env=env
            )
            
            # Ler saída em tempo real
            applied_count = 0
            error_count = 0
            
            while True:
                if not self.is_running:
                    break
                
                line = self.bot_process.stdout.readline()
                
                if not line:
                    # Processo terminou
                    break
                
                try:
                    # Remover códigos de cor ANSI
                    import re
                    clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                    
                    self.log_text.insert("end", clean_line)
                    self.log_text.see("end")
                    exec_window.update()  # Atualizar GUI em tempo real
                except Exception as e:
                    # Se falhar ao inserir, tenta limpar caracteres especiais
                    try:
                        clean_line = line.encode('ascii', 'ignore').decode('ascii')
                        self.log_text.insert("end", clean_line + "\n")
                        self.log_text.see("end")
                        exec_window.update()
                    except:
                        pass
                
                # Contar aplicações e erros
                if "Candidatura enviada" in line or "aplicado" in line.lower():
                    applied_count += 1
                elif "❌" in line or "erro" in line.lower():
                    error_count += 1
                
                # Atualizar estatísticas em tempo real
                try:
                    self.stats_label.configure(text=f"Vagas aplicadas: {applied_count} | Erros: {error_count}")
                    exec_window.update()
                except:
                    pass
            
            self.bot_process.wait()
            
            if self.is_running:
                self.log_text.insert("end", "\n✅ Bot finalizado!\n")
                self.log_text.insert("end", f"📊 Total de candidaturas: {applied_count}\n")
                self.log_text.see("end")
                self.status_label.configure(text="✅ Bot Finalizado", text_color="#4CAF50")
                self.cancel_btn.configure(text="✔️ Fechar", fg_color="#4CAF50")
                exec_window.update()
            
        except Exception as e:
            error_msg = f"\n❌ Erro: {str(e)}\n"
            try:
                self.log_text.insert("end", error_msg)
                self.log_text.see("end")
                exec_window.update()
            except:
                # Se falhar, tenta versão ASCII
                clean_msg = error_msg.encode('ascii', 'ignore').decode('ascii')
                self.log_text.insert("end", clean_msg)
                exec_window.update()
            self.status_label.configure(text="❌ Erro ao executar", text_color="#F44336")
    
    def stop_bot(self, exec_window):
        """Para o bot em execução"""
        if self.is_running and self.bot_process:
            if messagebox.askyesno("Confirmar", "Tem certeza que deseja parar o bot?"):
                self.is_running = False
                self.bot_process.terminate()
                self.log_text.insert("end", "\n\n⏹️ Bot parado pelo usuário\n")
                self.status_label.configure(text="⏹️ Bot Parado", text_color="#FF9800")
                self.cancel_btn.configure(text="✔️ Fechar", fg_color="#4CAF50")
        else:
            exec_window.destroy()
            self.window.deiconify()  # Mostrar janela principal novamente
    
    def on_closing_execution(self, exec_window):
        """Ao fechar janela de execução"""
        if self.is_running:
            if messagebox.askyesno("Confirmar", "O bot ainda está rodando. Deseja parar e fechar?"):
                self.stop_bot(exec_window)
        else:
            exec_window.destroy()
            self.window.deiconify()
    
    def run(self):
        """Inicia a interface"""
        self.window.mainloop()


if __name__ == "__main__":
    app = LinkedInBotGUI()
    app.run()
