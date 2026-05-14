import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, simpledialog
from services.gerenciador_tarefas import GerenciadorTarefas

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JanelaPrincipal(ctk.CTk):
    def __init__(self, gerenciador_usuarios):
        super().__init__()

        self.title("Gerenciador de Tarefas")
        self.geometry("800x650")
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.gerenciador_usuarios = gerenciador_usuarios
        self.gerenciador_tarefas = None
        
        self.container_principal = ctk.CTkFrame(self)
        self.container_principal.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.current_frame = None

        self.iniciar_login()
        
    def _mudar_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.container_principal, self, *args)
        self.current_frame.pack(fill="both", expand=True)

    def iniciar_login(self):
        self._mudar_frame(FrameLogin)

    def login(self, email, senha):
        if self.gerenciador_usuarios.login(email, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.gerenciador_tarefas = GerenciadorTarefas(self.gerenciador_usuarios.obter_usuario_logado())
            self.iniciar_tarefas()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    def iniciar_cadastro(self):
        self._mudar_frame(FrameCadastro)

    def cadastrar(self, nome, email, senha):
        if self.gerenciador_usuarios.cadastrar_usuario(nome, email, senha):
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.iniciar_login()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar o usuário.")

    def iniciar_tarefas(self):
        self._mudar_frame(FrameTarefas, self.gerenciador_tarefas)

    def deslogar(self):
        self.gerenciador_tarefas = None
        messagebox.showinfo("Deslogado", "Você saiu da sua conta.")
        self.iniciar_login()

    def excluir_conta(self):
        resposta = messagebox.askyesno("Confirmar", "Isso apagará todos os seus dados. Deseja continuar?")
        if resposta:
            resultado = self.gerenciador_usuarios.excluir_conta() 
            messagebox.showinfo("Conta Excluída", resultado)
            self.iniciar_login()

class FrameLogin(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Bem-vindo", font=("Roboto", 24, "bold")).grid(row=0, columnspan=2, pady=30)

        ctk.CTkLabel(self, text="Email:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="seu@email.com", width=250)
        self.email_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self, text="Senha:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.senha_entry = ctk.CTkEntry(self, show="*", placeholder_text="sua senha", width=250)
        self.senha_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.fazer_login, width=250)
        self.login_button.grid(row=3, columnspan=2, pady=30)

        self.cadastrar_button = ctk.CTkButton(self, text="Criar Conta", command=controller.iniciar_cadastro, fg_color="transparent", border_width=1, border_color="#3B8ED0")
        self.cadastrar_button.grid(row=4, columnspan=2)

    def fazer_login(self):
        email = self.email_entry.get()
        senha = self.senha_entry.get()
        self.controller.login(email, senha)

class FrameCadastro(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Criar Nova Conta", font=("Roboto", 24, "bold")).grid(row=0, columnspan=2, pady=30)

        ctk.CTkLabel(self, text="Nome:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.nome_entry = ctk.CTkEntry(self, placeholder_text="Seu nome completo", width=250)
        self.nome_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="seu@email.com", width=250)
        self.email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        ctk.CTkLabel(self, text="Senha:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.senha_entry = ctk.CTkEntry(self, show="*", placeholder_text="sua senha", width=250)
        self.senha_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        self.cadastrar_button = ctk.CTkButton(self, text="Cadastrar", command=self.fazer_cadastro, width=250)
        self.cadastrar_button.grid(row=4, columnspan=2, pady=30)

        self.voltar_button = ctk.CTkButton(self, text="Voltar ao Login", command=controller.iniciar_login, fg_color="transparent")
        self.voltar_button.grid(row=5, columnspan=2)

    def fazer_cadastro(self):
        nome = self.nome_entry.get().strip()
        email = self.email_entry.get().lower().strip()
        senha = self.senha_entry.get().strip()
        self.controller.cadastrar(nome, email, senha)

class FrameTarefas(ctk.CTkFrame):
    def __init__(self, parent, controller, gerenciador_tarefas):
        super().__init__(parent)
        self.controller = controller
        self.gerenciador_tarefas = gerenciador_tarefas
        self.tarefas_cache = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        ctk.CTkLabel(self, text="Minhas Tarefas", font=("Roboto", 24, "bold")).grid(row=0, column=0, pady=20)

        acoes_top_frame = ctk.CTkFrame(self, fg_color="transparent")
        acoes_top_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        self.add_button = ctk.CTkButton(acoes_top_frame, text="+ Nova Tarefa", command=self.adicionar_tarefa)
        self.add_button.pack(side="left", padx=5)
        
        self.btn_filtrar = ctk.CTkButton(acoes_top_frame, text="🔍 Filtrar", command=self.filtrar_tarefas, fg_color="#3B8ED0")
        self.btn_filtrar.pack(side="left", padx=5)

        self.btn_ordenar = ctk.CTkButton(acoes_top_frame, text="↕ Ordenar", command=self.ordenar_tarefas, fg_color="#3B8ED0")
        self.btn_ordenar.pack(side="left", padx=5)

        self.update_button = ctk.CTkButton(acoes_top_frame, text="🔄 Atualizar", command=self.listar_tarefas, fg_color="gray")
        self.update_button.pack(side="right", padx=5)

        lista_frame = ctk.CTkFrame(self)
        lista_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")


        self.lista_tarefas = tk.Listbox(
            lista_frame, 
            width=50, 
            height=12,
            bg="#2B2B2B", 
            fg="#FFFFFF", 
            selectbackground="#3B8ED0", 
            selectforeground="#FFFFFF",
            font=("Arial", 11),
            highlightthickness=0,
            bd=0
        )
        
        scrollbar = ctk.CTkScrollbar(lista_frame, command=self.lista_tarefas.yview)
        
        self.lista_tarefas.config(yscrollcommand=scrollbar.set)
        self.lista_tarefas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y", padx=5, pady=5)

        acoes_bot_frame = ctk.CTkFrame(self, fg_color="transparent")
        acoes_bot_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(acoes_bot_frame, text="📝 Editar", command=self.editar_tarefas, width=100)\
            .pack(side="left", padx=5)
        ctk.CTkButton(acoes_bot_frame, text="✅ Concluir", command=self.concluir_tarefa, fg_color="green", width=100)\
            .pack(side="left", padx=5)
        ctk.CTkButton(acoes_bot_frame, text="🗑️ Remover", command=self.remover_tarefa, fg_color="#FF3B3B", width=100)\
            .pack(side="left", padx=5)

        ctk.CTkButton(acoes_bot_frame, text="Sair", command=controller.deslogar, fg_color="gray", width=80)\
            .pack(side="right", padx=5)

        ctk.CTkButton(acoes_bot_frame, text="⚠️ Excluir Conta", command=controller.excluir_conta, 
                      fg_color="transparent", border_width=1, text_color="#FF3B3B", border_color="#FF3B3B", width=120)\
            .pack(side="right", padx=10)

        self.listar_tarefas()

    
    def adicionar_tarefa(self):
        descricao = simpledialog.askstring("Nova Tarefa", "Digite a descrição da tarefa:")
        if descricao:
            resultado = self.gerenciador_tarefas.adicionar_tarefa(descricao)
            messagebox.showinfo("Resultado", resultado)
            self.listar_tarefas()

    def obter_tarefa_selecionada(self):
        try:
            indice = self.lista_tarefas.curselection()[0]
            return self.tarefas_cache[indice]
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma tarefa primeiro.")
            return None

    def editar_tarefas(self):
        tarefa = self.obter_tarefa_selecionada()
        if tarefa:
            descricao = simpledialog.askstring("Nova Descrição", "Digite a nova descrição:")
            if descricao:
                resultado = self.gerenciador_tarefas.editar_tarefas(tarefa.id, descricao)
                messagebox.showinfo("Resultado", resultado)
                self.listar_tarefas()

    def concluir_tarefa(self):
        tarefa = self.obter_tarefa_selecionada()
        if tarefa:
            resultado = self.gerenciador_tarefas.concluir_tarefa(tarefa.id)
            messagebox.showinfo("Resultado", resultado)
            self.listar_tarefas()

    def remover_tarefa(self):
        tarefa = self.obter_tarefa_selecionada()
        if tarefa:
            resultado = self.gerenciador_tarefas.remover_tarefa(tarefa.id)
            messagebox.showinfo("Resultado", resultado)
            self.listar_tarefas()

    def filtrar_tarefas(self):
        condicao = simpledialog.askstring("Filtro", "Escolha o filtro [Pendente/Concluída]: ")
        if not condicao:
            return
        try:
            condicao = condicao.strip().capitalize()
            tarefas = self.gerenciador_tarefas.filtrar_tarefas(condicao)

            if isinstance(tarefas, str):
                messagebox.showinfo("Tarefas", tarefas)
                return

            self.atualizar_lista(tarefas)
        except Exception:
            self.listar_tarefas()
            
    def ordenar_tarefas(self):
        condicao = simpledialog.askstring("Ordem", "Escolha a ordem [ASC/DESC]: ")
        if not condicao:
            return
        try:
            condicao = condicao.strip().upper()
            tarefas = self.gerenciador_tarefas.ordenar_tarefas(condicao)

            if isinstance(tarefas, str):
                messagebox.showinfo("Tarefas", tarefas)
                return
            
            self.atualizar_lista(tarefas)
        except Exception:
            self.listar_tarefas()

    def listar_tarefas(self):
        tarefas = self.gerenciador_tarefas.listar_tarefas()
        if isinstance(tarefas, str):
            messagebox.showinfo("Tarefas", tarefas)
            self.lista_tarefas.delete(0, tk.END)
            return
        self.atualizar_lista(tarefas)

    def atualizar_lista(self, tarefas):
        import tkinter as tk 
        self.lista_tarefas.delete(0, tk.END)
        self.tarefas_cache = tarefas
        for tarefa in tarefas:
            self.lista_tarefas.insert(tk.END, str(tarefa))
