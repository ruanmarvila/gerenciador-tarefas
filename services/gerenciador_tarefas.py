from database.db import conectar
from models.tarefas import Tarefa

class GerenciadorTarefas:
    def __init__(self, usuario_logado=None):
        self.usuario_logado = usuario_logado


    def verificar_login(self):
        if not self.usuario_logado:
            raise Exception("Você precisa estar logado.")


    def adicionar_tarefa(self, descricao):
        try:
            self.verificar_login()
        except Exception as e:
            return f"❌ {e}"
    
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tarefas (descricao, concluida, usuario_id) VALUES (?, ?, ?)",
            (descricao, 0, self.usuario_logado.id)
        )
        conn.commit()
        conn.close()
        return "Tarefa adicionada."


    def editar_tarefas(self, tarefa_id ,descricao):
        try:
            self.verificar_login()
        except Exception as e:
            return f"Error: {e}"

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE tarefas SET descricao = ? WHERE id=? AND usuario_id=?",
            (descricao, tarefa_id, self.usuario_logado.id)
        )
        conn.commit()

        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return "Tarefa não encontrada."

        cursor.close()
        conn.close()
        return "Tarefa atualizada com sucesso!"


    def listar_tarefas(self):
        try:
            self.verificar_login()
        except Exception as e:
            return f"Error: {e}"

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tarefas WHERE usuario_id = ?",(self.usuario_logado.id,))
        rows = cursor.fetchall()
        conn.close()

        """if not rows:
            return "Nenhuma tarefa registrada."""

        return [Tarefa(id=row[0], descricao=row[1], concluida=bool(row[2])) for row in rows]


    def concluir_tarefa(self, tarefa_id):
        try:
            self.verificar_login()
        except Exception as e:
            return f"Error: {e}"
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT concluida FROM tarefas WHERE id = ? AND usuario_id = ?",
                       (tarefa_id, self.usuario_logado.id))
        resultado = cursor.fetchone()

        if resultado is None:
            conn.close()
            return "Tarefa não encontrada."

        if resultado[0] == 1:
            conn.close()
            return "A tarefa já estava concluída!"

        cursor.execute(
            "UPDATE tarefas SET concluida = 1 WHERE id = ?",
            (tarefa_id,)
        )
        conn.commit()
        conn.close()
        return "Tarefa Concluída!"


    def filtrar_tarefas(self, condicao):
        try:
            self.verificar_login()
        except Exception as e:
            return f"Error: {e}"
        
        if condicao not in ["Concluída", "Pendente"]:
            return False

        condicoes = {
            "Pendente": 0,
            "Concluída": 1
        }
        condicao = condicoes[condicao]
        
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tarefas WHERE concluida=? AND usuario_id=?", 
                       (condicao, self.usuario_logado.id))
        rows = cursor.fetchall()
        
        if not rows:
            conn.close()
            return "Nenhuma tarefa encontrada."

        conn.close()
        return [Tarefa(id=row[0], descricao=row[1], concluida=bool(row[2])) for row in rows]


    def ordenar_tarefas(self, ordem_user):
        if ordem_user.upper() not in ["ASC", "DESC"]:
            return False
        
        ordenacao = ordem_user.upper()
        
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(f"SELECT * FROM tarefas WHERE usuario_id=? ORDER BY descricao COLLATE NOCASE {ordenacao}",
                       (self.usuario_logado.id,))
        rows = cursor.fetchall()

        if not rows:
            conn.close()
            return "Nenhuma tarefa encontrada."

        conn.close()
        return [Tarefa(id=row[0], descricao=row[1], concluida=bool(row[2])) for row in rows]


    def remover_tarefa(self, tarefas_id):
        try:
            self.verificar_login()
        except Exception as e:
            return f"Error: {e}"
        
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tarefas WHERE id = ? AND usuario_id = ?",
                       (tarefas_id, self.usuario_logado.id))

        if cursor.rowcount == 0:
            conn.close()
            return "Tarefa não encontrada."

        conn.commit()
        conn.close()
        return "Tarefa Removida!"
