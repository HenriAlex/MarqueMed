from database.conexao import Conexao


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

        # Criação da tabela usuario
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT NOT NULL UNIQUE,
                cep TEXT,
                data_de_nascimento DATE,
                sexo TEXT,
                tipo TEXT,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                id_perfil INTEGER,
                FOREIGN KEY (id_perfil) REFERENCES perfil(id_perfil)
            );
            """
        )

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


if __name__ == "__main__":
    # Permite executar com `python -m database.criar_banco`
    CriarBanco.criar()
    print("Banco criado (ou já existente): MarqueMed.db")
