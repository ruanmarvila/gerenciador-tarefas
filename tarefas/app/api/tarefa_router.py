from fastapi import APIRouter, Depends, status

from app.core.dependencies import TaskServiceDep, UsuarioLogadoDep, obter_usuario_logado
from app.core.enums import ColunaTarefa, OrdemTarefa, StatusTarefa
from app.schemas import TarefaCreate, TarefaResponse, TarefaUpdate

tarefa_router = APIRouter(
    prefix="/api/v1/tarefas", 
    tags=["tarefas"], 
    dependencies=[Depends(obter_usuario_logado)]
)

@tarefa_router.post("/criar", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED)
async def criar(tarefa_schema: TarefaCreate, usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    return await session.criar_tarefa(tarefa_schema, usuario_logado)

@tarefa_router.get("/listar", response_model=list[TarefaResponse])
async def listar(usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    return await session.listar_tarefas(usuario_logado)

@tarefa_router.get("/listar/filtrada", response_model=list[TarefaResponse])
async def listar_filtrada(status: StatusTarefa, usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    return await session.lista_filtrada(status, usuario_logado)

@tarefa_router.get("/listar/ordenada", response_model=list[TarefaResponse])
async def listar_ordenada(coluna: ColunaTarefa, ordem: OrdemTarefa, usuario_logado: UsuarioLogadoDep, 
                          session: TaskServiceDep):
    return await session.lista_ordenada(coluna, ordem, usuario_logado)

@tarefa_router.patch("/editar/{tarefa_id}", response_model=TarefaResponse)
async def editar(tarefa_id: int, tarefa_schema: TarefaUpdate, usuario_logado: UsuarioLogadoDep, 
                 session: TaskServiceDep):
    return await session.editar_tarefa(tarefa_id, tarefa_schema, usuario_logado)

@tarefa_router.patch("/editar/status/{tarefa_id}", response_model=TarefaResponse)
async def editar_status(tarefa_id: int, status: StatusTarefa, usuario_logado: UsuarioLogadoDep, 
                   session: TaskServiceDep):
    return await session.editar_status(tarefa_id, status, usuario_logado)

@tarefa_router.delete("/excluir/{tarefa_id}", response_model=TarefaResponse)
async def excluir(tarefa_id: int, usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    return await session.excluir_tarefa(tarefa_id, usuario_logado)

@tarefa_router.get("/lixeira", response_model=list[TarefaResponse])
async def lixeira(usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    return await session.listar_tarefas_lixeira(usuario_logado)

@tarefa_router.patch("/restaurar/{tarefa_id}", response_model=TarefaResponse)
async def restaurar(tarefa_id: int, usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    return await session.recuperar_tarefa(tarefa_id, usuario_logado)

@tarefa_router.delete("/lixeira/esvaziar", status_code=status.HTTP_204_NO_CONTENT)
async def esvaziar_lixeira(usuario_logado: UsuarioLogadoDep, session: TaskServiceDep):
    await session.esvaziar_lixeria(usuario_logado)