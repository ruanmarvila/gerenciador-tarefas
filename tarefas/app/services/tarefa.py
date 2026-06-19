from app.core.enums import ColunaTarefa, OrdemTarefa, StatusTarefa
from app.exceptions import AcessoNegadoError, TarefaNaoEncontradaError
from app.models import Tarefa, Usuario
from app.repositories import TarefaRepository
from app.schemas import TarefaCreate, TarefaUpdate


class TarefaService:
    
    def __init__(self, repo: TarefaRepository) -> None:
        self.repo = repo

    async def criar_tarefa(self, tarefa_schema: TarefaCreate, usuario_logado: Usuario) -> Tarefa:
        nova_tarefa = Tarefa(usuario_id=usuario_logado.id,
                             titulo=tarefa_schema.titulo,
                             descricao=tarefa_schema.descricao)
        
        return await self.repo.adicionar(nova_tarefa)
    
    async def listar_tarefas(self, usuario_logado: Usuario) -> list[Tarefa]:
        lista_tarefas = await self.repo.buscar(usuario_logado.id)
        
        if not lista_tarefas:
            raise TarefaNaoEncontradaError()
        
        return lista_tarefas
    
    async def listar_tarefas_lixeira(self, usuario_logado: Usuario) -> list[Tarefa]:
        lista_tarefas = await self.repo.buscar_excluidas(usuario_logado.id)

        if not lista_tarefas:
            raise TarefaNaoEncontradaError()
        
        return lista_tarefas
    
    async def lista_filtrada(self, status: StatusTarefa, usuario_logado: Usuario) -> list[Tarefa]:
        lista_tarefas = await self.repo.buscar_por_status(status, usuario_logado.id)

        if not lista_tarefas:
            raise TarefaNaoEncontradaError()
        
        return lista_tarefas
    
    async def lista_ordenada(self, coluna: ColunaTarefa, sort: OrdemTarefa, 
                             usuario_logado: Usuario) -> list[Tarefa]:
        
        lista_tarefas = await self.repo.busca_ordenada(coluna, sort, usuario_logado.id)

        if not lista_tarefas:
            raise TarefaNaoEncontradaError()
        
        return lista_tarefas
    
    async def editar_tarefa(self, tarefa_id: int, tarefa_schema: TarefaUpdate, 
                            usuario_logado: Usuario) -> Tarefa:
        tarefa = await self.repo.buscar_por_id(tarefa_id)

        if not tarefa:
            raise TarefaNaoEncontradaError()

        if tarefa.usuario_id != usuario_logado.id:
            raise AcessoNegadoError()
        
        dados = tarefa_schema.model_dump(exclude_unset=True)
        
        return await self.repo.editar_tarefa(tarefa, **dados)
    
    async def editar_status(self, tarefa_id: int, status: StatusTarefa, usuario_logado: Usuario) -> Tarefa:
        tarefa = await self.repo.buscar_por_id(tarefa_id)

        if not tarefa:
            raise TarefaNaoEncontradaError()
        
        if tarefa.usuario_id != usuario_logado.id:
            raise AcessoNegadoError()
        
        return await self.repo.editar_status(tarefa, status)
    
    async def excluir_tarefa(self, tarefa_id: int, usuario_logado: Usuario) -> Tarefa:
        tarefa = await self.repo.buscar_por_id(tarefa_id)

        if not tarefa:
            raise TarefaNaoEncontradaError()
        
        if tarefa.usuario_id != usuario_logado.id:
            raise AcessoNegadoError()
        
        return await self.repo.excluir_tarefa(tarefa)
    
    async def recuperar_tarefa(self, tarefa_id: int, usuario_logado: Usuario) -> Tarefa:
        tarefa = await self.repo.buscar_excluida_por_id(tarefa_id)

        if not tarefa:
            raise TarefaNaoEncontradaError()
        
        if tarefa.usuario_id != usuario_logado.id:
            raise AcessoNegadoError()
        
        return await self.repo.recuperar_tarefa(tarefa)
    
    async def esvaziar_lixeria(self, usuario_logado: Usuario) -> None:
        lista_tarefas = await self.repo.buscar_excluidas(usuario_logado.id)

        if not lista_tarefas:
            raise TarefaNaoEncontradaError()
        
        for tarefa in lista_tarefas:
            await self.repo.deletar(tarefa)