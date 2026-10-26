# Importa o APIRouter e a exceção HTTP.
# O APIRouter permite criar e organizar as rotas da API.
from fastapi import APIRouter, HTTPException
import sqlite3

from models.usuario import usuario
from schema.usuario_schema import UsuarioSchema, LoginSchema
from service.usuario_service import UsuarioService


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


service = UsuarioService()


# Converte erros de regra de negócio e de banco (ex.: RA ou e-mail
# duplicado) em resposta 400 com a mensagem em "detail",
# que é o formato que o front-end exibe ao usuário.
def _erro_400(erro):
    if isinstance(erro, sqlite3.IntegrityError):
        return HTTPException(status_code=400, detail="ID do paciente, CPF ou e-mail já cadastrado.")
    return HTTPException(status_code=400, detail=str(erro))


# Monta o Model a partir do Schema recebido na requisição.
def _montar_usuario(usuario_schema: UsuarioSchema, id_usuario=0):
    return usuario(
        id_usuario=id_usuario,
        ra=usuario_schema.ra,
        cpf=usuario_schema.cpf,
        cep=usuario_schema.cep,
        sexo=usuario_schema.sexo,
        data_de_nascimento=usuario_schema.data_de_nascimento,
        nome=usuario_schema.nome,
        id_perfil=usuario_schema.id_perfil,
        email=usuario_schema.email,
        senha=usuario_schema.senha,
    )


# ============================================================
# LISTAR USUÁRIOS
# ============================================================

@router.get("/")
def listar():
    return service.listar()


# ============================================================
# LOGIN
# ============================================================

# Valida e-mail e senha. Não devolve a senha na resposta.
@router.post("/login")
def login(login_schema: LoginSchema):
    try:
        usuario_logado = service.login(login_schema.email, login_schema.senha)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))

    return {
        "id_usuario": usuario_logado.id_usuario,
        "ra": usuario_logado.ra,
        "nome": usuario_logado.nome,
        "email": usuario_logado.email,
        "id_perfil": usuario_logado.id_perfil,
        "ds_perfil": usuario_logado.ds_perfil,
    }


# ============================================================
# CADASTRAR USUÁRIO
# ============================================================

# Define a rota POST para cadastrar um usuário.
@router.post("/")
def cadastrar(usuario_schema: UsuarioSchema):
    try:
        service.cadastrar(_montar_usuario(usuario_schema))
    except (ValueError, sqlite3.IntegrityError) as erro:
        raise _erro_400(erro)

    return {"mensagem": "Usuário cadastrado com sucesso."}


# ============================================================
# ATUALIZAR USUÁRIO
# ============================================================

@router.put("/{id_usuario}")
def atualizar(id_usuario: int, usuario_schema: UsuarioSchema):
    try:
        service.atualizar(_montar_usuario(usuario_schema, id_usuario))
    except (ValueError, sqlite3.IntegrityError) as erro:
        raise _erro_400(erro)

    return {"mensagem": "Usuário atualizado com sucesso."}


# ============================================================
# EXCLUIR USUÁRIO
# ============================================================

@router.delete("/{id_usuario}")
def excluir(id_usuario: int):
    try:
        service.excluir(id_usuario)
    except ValueError as erro:
        raise _erro_400(erro)

    return {"mensagem": "Usuário removido com sucesso."}
