# Importa o BaseModel do Pydantic.
# O FastAPI utiliza o Pydantic para validar
# os dados recebidos nas requisições.
from pydantic import BaseModel
from datetime import date
from typing import Optional


class UsuarioSchema(BaseModel):
    # Identificador do paciente ("ID do paciente" no front-end).
    ra: str
    nome: str
    email: str
    senha: str
    id_perfil: Optional[int] = None

    # Campos opcionais: nem todas as telas os enviam.
    cpf: Optional[str] = None
    cep: Optional[str] = None
    sexo: Optional[str] = None
    data_de_nascimento: Optional[date] = None


class LoginSchema(BaseModel):
    email: str
    senha: str
