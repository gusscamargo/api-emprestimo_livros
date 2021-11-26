class ConexaoServidor:
    def __init__(self):
        self.usuario = "root"
        self.senha = ""
        self.endereco = "127.0.0.1"
        self.porta = "3306"
        self.nomeBanco = "emprestimo_livros"

    def getConfig(self):
        return "mysql+pymysql://{:}:{:}@{:}:{:}/{:}".format(self.usuario, self.senha, self.endereco, self.porta, self.nomeBanco)
