from database.conexao import conexao
from models.perfil import Perfil


class PerfilRepository:
    def inserir(self, perfil: Perfil):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO perfil (ds_perfil) VALUES (?)
            """,
            (perfil.ds_perfil,)
        )
        conn.commit()
        conn.close()

    def listar(self):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_perfil, ds_perfil FROM perfil")
        rows = cursor.fetchall()
        conn.close()
        return [Perfil(id_perfil=row[0], ds_perfil=row[1]) for row in rows]

    def buscar_por_id(self, id_perfil):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id_perfil, ds_perfil FROM perfil WHERE id_perfil = ?", (id_perfil,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return Perfil(id_perfil=row[0], ds_perfil=row[1])

    def possui_usuarios(self, id_perfil):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuario WHERE id_perfil = ? LIMIT 1", (id_perfil,))
        existe = cursor.fetchone() is not None
        conn.close()
        return existe

    def excluir(self, id_perfil):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM perfil WHERE id_perfil = ?", (id_perfil,))
        conn.commit()
        conn.close()
    
    def atualizar(self, perfil: Perfil):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE perfil SET ds_perfil = ? WHERE id_perfil = ?",
            (perfil.ds_perfil, perfil.id_perfil)
        )
        conn.commit()
        conn.close()