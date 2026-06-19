from sqlalchemy import asc, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.enums import ColunaTarefa, OrdemTarefa, StatusTarefa
from app.models import Tarefa


class TarefaRepository:

    COLUNA_MAPA = {
            ColunaTarefa.TITULO: Tarefa.titulo,
            ColunaTarefa.CRIACAO: Tarefa.criado_em,
            ColunaTarefa.ATUALIZACAO: Tarefa.atualizado_em
        }
    
    ORDEM_MAPA = {
        OrdemTarefa.ASCENDENTE: asc,
        OrdemTarefa.DESCENDENTE: desc
    }
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def buscar(self, usuario_id: int) -> list[Tarefa]:
        lista_tarefas = await self.session.execute(
            select(Tarefa).where(Tarefa.usuario_id == usuario_id, 
                                 Tarefa.deletado_em.is_(None))
        )
        return list(lista_tarefas.scalars().all())
    
    async def buscar_por_id(self, tarefa_id: int) -> Tarefa | None:
        tarefa = await self.session.execute(
            select(Tarefa).where(Tarefa.id == tarefa_id, 
                                 Tarefa.deletado_em.is_(None))
        )
        return tarefa.scalar_one_or_none()
    
    async def buscar_por_status(self, status: StatusTarefa, usuario_id: int) -> list[Tarefa]:
        lista_tarefas = await self.session.execute(
            select(Tarefa).where(Tarefa.usuario_id == usuario_id, 
                                 Tarefa.status == status, 
                                 Tarefa.deletado_em.is_(None))
        )
        return list(lista_tarefas.scalars().all())
    
    async def busca_ordenada(self, coluna: ColunaTarefa, ordem: OrdemTarefa, usuario_id: int) -> list[Tarefa]:
        ordem_coluna = self.ORDEM_MAPA[ordem](self.COLUNA_MAPA[coluna])

        lista_ordenada = await self.session.execute(
            select(Tarefa).where(Tarefa.usuario_id == usuario_id,
                                 Tarefa.deletado_em.is_(None)
                                 ).order_by(ordem_coluna)
        )
        return list(lista_ordenada.scalars().all())
    
    async def buscar_excluidas(self, usuario_id: int) -> list[Tarefa]:
        lista_tarefas = await self.session.execute(
            select(Tarefa).where(Tarefa.usuario_id == usuario_id, 
                                 Tarefa.deletado_em.is_not(None))
        )
        return list(lista_tarefas.scalars().all())

    async def buscar_excluida_por_id(self, tarefa_id: int) -> Tarefa | None:
        tarefa = await self.session.execute(
            select(Tarefa).where(Tarefa.id == tarefa_id,
                                 Tarefa.deletado_em.is_not(None))
        )
        return tarefa.scalar_one_or_none()
    
    async def editar_status(self, tarefa: Tarefa, status: StatusTarefa):
        tarefa.status = status
        await self.session.flush()
        await self.session.refresh(tarefa)
        return tarefa
    
    async def editar_tarefa(self, tarefa: Tarefa, **dados) -> Tarefa:
        for campo, valor in dados.items():
            setattr(tarefa, campo, valor)

        self.session.add(tarefa)
        await self.session.flush()
        await self.session.refresh(tarefa)
        return tarefa
    
    async def excluir_tarefa(self, tarefa: Tarefa) -> Tarefa:
        tarefa.deletado_em = func.now()
        return tarefa
    
    async def recuperar_tarefa(self, tarefa: Tarefa) -> Tarefa:
        tarefa.deletado_em = None
        return tarefa

    async def adicionar(self, tarefa: Tarefa) -> Tarefa:
        self.session.add(tarefa)
        await self.session.flush()
        await self.session.refresh(tarefa)
        return tarefa
    
    async def deletar(self, tarefa: Tarefa) -> None:
        await self.session.delete(tarefa)