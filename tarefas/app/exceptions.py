class ModelError(Exception):
    def __init__(self, mensagem: str):
        self.mensagem = mensagem

class AcessoNegadoError(ModelError):
    def __init__(self, mensagem = "Acesso Negado"):
        super().__init__(mensagem)

class UsuarioNaoEncontradoError(ModelError):
    def __init__(self, mensagem = "Usuário não encontrado"):
        super().__init__(mensagem)

class TarefaNaoEncontradaError(ModelError):
    def __init__(self, mensagem = "Tarefa(s) não encontrada(s)"):
        super().__init__(mensagem)

class EmailDuplicadoError(ModelError):
    def __init__(self, mensagem= "Já existe um usuário com esse email"):
        super().__init__(mensagem)
    
class CredenciaisInvalidasError(ModelError):
    def __init__(self, mensagem = "Credenciais Inválidas"):
        super().__init__(mensagem)

class TokenInvalidoError(ModelError):
    def __init__(self, mensagem = "Token inválido"):
        super().__init__(mensagem)

class UsuarioAtivoError(ModelError):
    def __init__(self, mensagem = "Usuário já está ativo"):
        super().__init__(mensagem)

class TokenExpiradoError(ModelError):
    def __init__(self, mensagem = "Token expirado"):
        super().__init__(mensagem)
