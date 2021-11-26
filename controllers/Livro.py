from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request
import enum
from model import *

app = Flask(__name__)
db = SQLAlchemy(app)

livro_schema = LivrosSchema()
livros_schema = LivrosSchema(many=True)

livrosUsuario_schema = UsuarioTemLivroSchema(many=True)


class Status(enum.Enum):
    DISPONIVEL = 0
    EMPRESTADO = 1
    VENDIDO = 2
    TROCADO = 3

class BancoLivro:
    def addLivro(request):

        novoLivro = Livro(
            request.json['autor'],
            request.json['titulo'],
            request.json['editora'],
            request.json['preco'],
            Status.DISPONIVEL
        )

        db.session.add(novoLivro)
        db.session.commit()
        db.session.close()

        return jsonify({"status": "successful"})

    def getLivros():
        livros = Livro.query.all()
        result = livros_schema.dump(livros)

        return jsonify(result)

    def getLivrosUsuario(id):
        livros = UsuarioTemLivro.query.filter_by(usuario_id=id).all()

        resultado = livrosUsuario_schema.dump(livros)

        return jsonify(resultado)

    def emprestarLivro(request):
        emprestimo = UsuarioTemLivro(
            usuario=request.json["usuario_id"],
            livro=request.json["livro_id"]
        )

        db.session.add(emprestimo)
        db.session.commit()
        db.session.close()

        return jsonify({"status": "successful"})
