from models.perfil import Perfil
from repositories.perfil_repository import PerfilRepository


class PerfilService:
    def __init__(self):
        self.repository = PerfilRepository()

    def cadastrar(self, perfil: Perfil):
        if not perfil.ds_perfil:
            raise ValueError("A descrição do perfil é obrigatória.")

        perfis = self.repository.listar()
        for perfil_existente in perfis:
            if perfil_existente.ds_perfil.lower() == perfil.ds_perfil.lower():
                raise ValueError("Já existe um perfil com esta descrição.")

        self.repository.inserir(perfil)

    def listar(self):
        return self.repository.listar()

    def buscar_por_id(self, id_perfil):
        if not id_perfil:
            raise ValueError("O ID do perfil é obrigatório.")
        perfil = self.repository.buscar_por_id(id_perfil)
        if not perfil:
            raise ValueError("Perfil não encontrado.")
        return perfil

    def atualizar(self, perfil: Perfil):
        if not perfil.id_perfil:
            raise ValueError("O ID do perfil é obrigatório.")
        if not perfil.ds_perfil:
            raise ValueError("A descrição do perfil é obrigatória.")
        perfil_existente = self.repository.buscar_por_id(perfil.id_perfil)
        if not perfil_existente:
            raise ValueError("Perfil não encontrado.")
        perfis = self.repository.listar()
        for perfil_item in perfis:
            if (perfil_item.ds_perfil.lower() == perfil.ds_perfil.lower() and perfil_item.id_perfil != perfil.id_perfil):
                raise ValueError("Já existe outro perfil com esta descrição.")
        self.repository.atualizar(perfil)

    def excluir(self, id_perfil):
        if not id_perfil:
            raise ValueError("O ID do perfil é obrigatório.")
        perfil = self.repository.buscar_por_id(id_perfil)
        if not perfil:
            raise ValueError("Perfil não encontrado.")
        # Evita deixar usuários apontando para um perfil removido.
        if self.repository.possui_usuarios(id_perfil):
            raise ValueError("Não é possível remover: existem usuários com este perfil.")
        self.repository.excluir(id_perfil)