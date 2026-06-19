# Gerenciador de Tarefas:

Uma API RESTful assíncrona para o gerenciamento de tarefas, construída com Python e FastAPI. Esse é um projeto de estudo com foco de aprendizado em fundamentos da web, APIs RESTful, Modelagem de Banco de Dados, Estruturação de Pastas.

## Funcionalidades:

- **Cadastro & Login:** Criação de conta e autenticação via JWT.
- **Gerenciamento de Conta:** Opção de editar a conta e desativá-la (*soft delete*).
- **Tarefas:** Criar, Listar, Editar e Excluir tarefas.
- **Lixeira:** Permite o usuário a recuperar tarefas excluídas.

## Tecnologias Utilizadas:

- **Python 3.14**
- **FastAPI:** Framework web moderno.
- **SQLite + Aiosqlite:** Banco de dados local.
- **SQLAlchemy + Alembic:** ORM para comunicação com o banco e controle de migração.
- **PyJWT e Argon2:** Criptografia de senha e geração de tokens.

## Próximos Passos:

- [ ] Juntar o ```/listar/filtrada``` e o ```/listar/ordenada``` num endpoint.
- [ ] Desenvolver o ```tests/``` para os teste unitários da aplicação.

## Estrutura do Projeto:
```
.
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── exceptions.py
│   └── main.py
│
├── .env
├── alembic.ini
├── README.md
└── requirements.txt
```

## Como Rodar o Projeto Localmente:

### Pré-requisitos:
- Python insatalado na máquina.

### Passo a Passo:

1. **Clone o Repositório:**

```bash
    git clone https://github.com/ruanmarvila/gerenciador-tarefas
```

2. **Crie um ambiente virtual:**

```bash
    python -m venv .venv

    # Windows:
    .venv\Scripts\Activate.ps1

    # Linux ou Mac:
    source .venv/bin/activate
```

3. **Instale as dependências:**

```bash
    pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Crie um .env na raiz
```properties
    SECRET_KEY=sua_chave_secreta_aqui
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. **Rode as migrações:**
```bash
    alembic upgrade head
```

6. **Inicie o servidor:**
```bash
    uvicorn app.main:app --reload
```

## Documentação da API:

O FastAPI cria automaticamente uma documentação interativa. Com o servidor rodando, você pode acessar e testar os endpoints através dos links:
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc