# Importa o FastAPI.
# Ele será utilizado para criar nossa aplicação.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# Importa a criação das tabelas do banco.
from database.criar_banco import CriarBanco


# Importa o Controller de usuários.
from controllers.usuario_controller import router as usuario_router


# Importa o Controller de perfis.
from controllers.perfil_controller import router as perfil_router


# Garante que as tabelas existam (e estejam atualizadas)
# antes de a API receber requisições.
CriarBanco.criar()


# Cria a aplicação FastAPI.
app = FastAPI(
    title="MarqueMed - API",
    description="API do sistema Saidinha",
    version="1.0.0"
)


# Libera o acesso do front-end (abre por arquivo ou outro endereço)
# às rotas da API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Adiciona as rotas relacionadas aos usuários
# à aplicação principal.
app.include_router(usuario_router)


# Adiciona as rotas relacionadas aos perfis
# à aplicação principal.
app.include_router(perfil_router)


# Cria uma rota simples para verificar
# se a API está funcionando.
@app.get("/")
def inicio():

    # Retorna uma mensagem.
    return {
        "mensagem": "API MarqueMed funcionando!"
    }