# Importa o APIRouter e a exceção HTTP.
from fastapi import APIRouter, HTTPException


# Importa o Model Perfil.
from models.perfil import Perfil


# Importa o Schema utilizado pela API.
from schema.perfil_schema import PerfilSchema


# Importa o Service de Perfil.
from service.perfil_service import PerfilService


# Cria as rotas dos perfis.
router = APIRouter(
    prefix="/perfis",
    tags=["Perfis"]
)


# Cria uma instância do Service.
service = PerfilService()


# Converte erros de regra de negócio em resposta 400 com "detail",
# formato que o front-end exibe ao usuário.
def _erro_400(erro):
    return HTTPException(status_code=400, detail=str(erro))


# ============================================================
# LISTAR PERFIS
# ============================================================

@router.get("/")
def listar():
    return service.listar()


# ============================================================
# CADASTRAR PERFIL
# ============================================================

# Define a rota POST.
@router.post("/")
def cadastrar(perfil_schema: PerfilSchema):

    # Cria um objeto do Model Perfil.
    perfil = Perfil(

        # Transfere a descrição recebida
        # pelo Schema para o Model.
        ds_perfil=perfil_schema.ds_perfil
    )

    # Envia o Model para o Service.
    try:
        service.cadastrar(perfil)
    except ValueError as erro:
        raise _erro_400(erro)

    # Retorna uma mensagem de sucesso.
    return {
        "mensagem": "Perfil cadastrado com sucesso."
    }


# ============================================================
# ATUALIZAR PERFIL
# ============================================================

@router.put("/{id_perfil}")
def atualizar(id_perfil: int, perfil_schema: PerfilSchema):
    perfil = Perfil(id_perfil=id_perfil, ds_perfil=perfil_schema.ds_perfil)
    try:
        service.atualizar(perfil)
    except ValueError as erro:
        raise _erro_400(erro)

    return {"mensagem": "Perfil atualizado com sucesso."}


# ============================================================
# EXCLUIR PERFIL
# ============================================================

@router.delete("/{id_perfil}")
def excluir(id_perfil: int):
    try:
        service.excluir(id_perfil)
    except ValueError as erro:
        raise _erro_400(erro)

    return {"mensagem": "Perfil removido com sucesso."}
