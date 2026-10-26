from database.conexao import Conexao


# SQL da tabela usuario.
# - ra: identificador do paciente enviado pelo front-end ("ID do paciente").
# - cpf: opcional (o front-end não envia), mas único quando informado.
#   Múltiplos NULL são aceitos pelo UNIQUE do SQLite.
SQL_USUARIO = """
    CREATE TABLE usuario (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        ra TEXT UNIQUE,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE,
        cep TEXT,
        data_de_nascimento TEXT,
        sexo TEXT,
        tipo TEXT,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        id_perfil INTEGER,
        FOREIGN KEY (id_perfil) REFERENCES perfil(id_perfil)
    );
"""


class CriarBanco:
    @staticmethod
    def criar():
        # Abre conexão
        conexao = Conexao.conectar()

        # Cria um cursor para executar comandos SQL.
        cursor = conexao.cursor()

        # Criação da tabela perfil (nome em minúsculas para consistência)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS perfil (
                id_perfil INTEGER PRIMARY KEY AUTOINCREMENT,
                ds_perfil TEXT NOT NULL
            );
            """
        )

        # Criação ou atualização da tabela usuario
        CriarBanco._criar_ou_migrar_usuario(cursor)

        # Criação da tabela especialidade
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS especialidade (
                id_especialidade INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_especialidade TEXT NOT NULL
            );
            """
        )

        # Salva as alterações e fecha a conexão
        conexao.commit()
        conexao.close()

    @staticmethod
    def _criar_ou_migrar_usuario(cursor):
        # PRAGMA table_info retorna (cid, nome, tipo, notnull, default, pk).
        colunas = cursor.execute("PRAGMA table_info(usuario)").fetchall()

        # Tabela inexistente: cria direto no formato atual.
        if not colunas:
            cursor.execute(SQL_USUARIO)
            return

        nomes = {coluna[1]: coluna[3] for coluna in colunas}

        # Tabela já está no formato atual (tem ra e cpf aceita NULL).
        if "ra" in nomes and nomes["cpf"] == 0:
            return

        # Tabela antiga (sem ra ou com cpf obrigatório): o SQLite não
        # altera restrições de coluna, então recria a tabela e copia
        # os dados existentes para não perder cadastros.
        cursor.execute("ALTER TABLE usuario RENAME TO usuario_antigo")
        cursor.execute(SQL_USUARIO)
        cursor.execute(
            """
            INSERT INTO usuario (
                id_usuario, nome, cpf, cep, data_de_nascimento,
                sexo, tipo, email, senha, id_perfil
            )
            SELECT
                id_usuario, nome, cpf, cep, data_de_nascimento,
                sexo, tipo, email, senha, id_perfil
            FROM usuario_antigo
            """
        )
        cursor.execute("DROP TABLE usuario_antigo")


if __name__ == "__main__":
    # Permite executar com `python -m database.criar_banco`
    CriarBanco.criar()
    print("Banco criado (ou já existente): MarqueMed.db")
