class usuario:
    def __init__(self,
                 id_usuario=0,
                 ra=None,
                 cpf=None,
                 cep=None,
                 nome="",
                 id_perfil=0,
                 email="",
                 senha="",
                 data_de_nascimento=None,
                 sexo=None,
                 tipo=None,
                 ds_perfil=""):

        self.id_usuario = id_usuario
        self.ra = ra
        self.cpf = cpf
        self.cep = cep
        self.nome = nome
        self.id_perfil = id_perfil
        self.ds_perfil = ds_perfil
        self.email = email
        self.senha = senha
        self.sexo = sexo
        self.tipo = tipo

        # Data não informada fica como NULL no banco.
        self.data_de_nascimento = data_de_nascimento
