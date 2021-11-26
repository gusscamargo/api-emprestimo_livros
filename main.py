from flask import Flask, render_template, request
from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy

from Usuario import BancoUsuario
from Livro import BancoLivro
from Endereco import BancoEndereco
from config import ConexaoServidor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ConexaoServidor().getConfig()
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        pass
    else:
        return render_template("index.html")

@app.route("/usuario", methods=["POST"])
def addUsuario():
    return BancoUsuario.addUsuario(request=request)  
    
@app.route("/livro", methods=["POST"])
def addLivro():
    return BancoLivro.addLivro(request=request)

@app.route("/livro", methods=["GET"])
def getLivros():
    return BancoLivro.getLivros()

@app.route("/emprestimo", methods=["POST"])
def emprestarLivro():
    return BancoLivro.emprestarLivro(request=request)

@app.route("/usuario/livro/<int:id>")
def getLivroUsuario(id):
    return BancoLivro.getLivrosUsuario(id)

@app.route("/endereco", methods=["POST"])
def addEndereco():
    return BancoEndereco.addEndereco(request=request)

@app.route("/endereco/<int:id>", methods=["GET"])
def getEnderecoUsuario(id):
    return BancoEndereco.getEnderecoUsuario(id)

@app.route("/login", methods=["POST"])
def login():
    return BancoUsuario.login(request=request)





if __name__ == '__main__':
    app.run(debug=True)
