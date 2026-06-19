import enum


class StatusTarefa(enum.StrEnum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDO = "concluido"

    @property
    def formatado(self):
        MAPA_FORMATADO = {
            StatusTarefa.PENDENTE: "Pendente",
            StatusTarefa.EM_ANDAMENTO: "Em Andamento",
            StatusTarefa.CONCLUIDO: "Concluído",
        }
        return MAPA_FORMATADO.get(self, self.value)
    
class ColunaTarefa(enum.StrEnum):
    TITULO = "titulo"
    CRIACAO = "criado_em"
    ATUALIZACAO = "atualizado_em"

class OrdemTarefa(enum.StrEnum):
    ASCENDENTE = "asc"
    DESCENDENTE = "desc"