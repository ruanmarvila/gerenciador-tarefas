from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api import auth_router, tarefa_router, usuario_router
from app.exceptions import (
    AcessoNegadoError,
    CredenciaisInvalidasError,
    EmailDuplicadoError,
    ModelError,
    TarefaNaoEncontradaError,
    TokenExpiradoError,
    TokenInvalidoError,
    UsuarioAtivoError,
    UsuarioNaoEncontradoError,
)

app = FastAPI(
    title="Gerenciador de Tarefas"
    )

MAPA_ERROR_HTTP = {
    TokenInvalidoError: status.HTTP_401_UNAUTHORIZED,
    CredenciaisInvalidasError: status.HTTP_401_UNAUTHORIZED,
    AcessoNegadoError: status.HTTP_403_FORBIDDEN,
    TarefaNaoEncontradaError: status.HTTP_404_NOT_FOUND,
    UsuarioNaoEncontradoError: status.HTTP_404_NOT_FOUND,
    EmailDuplicadoError: status.HTTP_409_CONFLICT,
    UsuarioAtivoError: status.HTTP_409_CONFLICT,
    TokenExpiradoError: status.HTTP_410_GONE
}

@app.exception_handler(ModelError)
async def model_error_handler(request: Request, exc: ModelError) -> JSONResponse:
    status_code = MAPA_ERROR_HTTP.get(type(exc), status.HTTP_400_BAD_REQUEST)

    return JSONResponse(
        status_code= status_code,
        content={"detail": exc.mensagem}
    )

app.include_router(auth_router)
app.include_router(tarefa_router)
app.include_router(usuario_router)



# uvicorn app.main:app --reload