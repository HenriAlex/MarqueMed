from database.conexao import conexao
from models.usuario import usuario


# Consulta base: já traz o nome do perfil para o front-end exibir.
SQL_SELECT = """
    SELECT u.id_usuario, u.ra, u.cpf, u.cep, u.nome, u.id_perfil,
           p.ds_perfil, u.email, u.senha, u.data_de_nascimento, u.sexo, u.tipo
    FROM usuario u
    LEFT JOIN perfil p ON p.id_perfil = u.id_perfil
"""


def _data_para_banco(data):
    # Converte a data para texto; None continua None (NULL no banco).
    return str(data) if data is not None else None


def _cpf_para_banco(cpf):
    # Texto vazio vira NULL para não violar o UNIQUE do CPF.
    return cpf or None


def _linha_para_usuario(row):
    return usuario(
        id_usuario=row[0],
        ra=row[1],
        cpf=row[2],
        cep=row[3],
        nome=row[4],
        id_perfil=row[5],
        ds_perfil=row[6] or "",
        email=row[7],
        senha=row[8],
        data_de_nascimento=row[9],
        sexo=row[10],
        tipo=row[11],
    )


class UsuarioRepository:
    def inserir(self, usuario: usuario):
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO usuario (
                    ra, cpf, cep, nome, id_perfil, email, senha, data_de_nascimento, sexo, tipo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    usuario.ra,
                    _cpf_para_banco(usuario.cpf),
                    usuario.cep,
                    usuario.nome,
                    usuario.id_perfil,
                    usuario.email,
                    usuario.senha,
                    _data_para_banco(usuario.data_de_nascimento),
                    usuario.sexo,
                    usuario.tipo,
                ),
            )
            conn.commit()
        finally:
            conn.close()

    def buscar_por_email(self, email):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(SQL_SELECT + " WHERE u.email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return _linha_para_usuario(row)

    def listar(self):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(SQL_SELECT + " ORDER BY u.nome")
        rows = cursor.fetchall()
        conn.close()
        return [_linha_para_usuario(row) for row in rows]

    def buscar_por_id(self, id_usuario):
        conn = conexao.conectar()
        cursor = conn.cursor()
        cursor.execute(SQL_SELECT + " WHERE u.id_usuario = ?", (id_usuario,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        return _linha_para_usuario(row)

    def excluir(self, id_usuario):
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
        finally:
            conn.close()

    def atualizar(self, usuario: usuario):
        # COALESCE mantém o valor atual quando o campo opcional não foi enviado
        # (ex.: o formulário de edição não envia cpf, cep, sexo, tipo nem data).
        conn = conexao.conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE usuario SET
                    ra = ?,
                    cpf = COALESCE(?, cpf),
                    cep = COALESCE(?, cep),
                    nome = ?,
                    id_perfil = ?,
                    email = ?,
                    senha = ?,
                    data_de_nascimento = COALESCE(?, data_de_nascimento),
                    sexo = COALESCE(?, sexo),
                    tipo = COALESCE(?, tipo)
                WHERE id_usuario = ?
                """,
                (
                    usuario.ra,
                    _cpf_para_banco(usuario.cpf),
                    usuario.cep,
                    usuario.nome,
                    usuario.id_perfil,
                    usuario.email,
                    usuario.senha,
                    _data_para_banco(usuario.data_de_nascimento),
                    usuario.sexo,
                    usuario.tipo,
                    usuario.id_usuario,
                ),
            )
            conn.commit()
        finally:
            conn.close()
