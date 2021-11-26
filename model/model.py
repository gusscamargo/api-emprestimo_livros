from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os, enum

from config import ConexaoServidor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ConexaoServidor().getConfig()
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Usuario(db.Model):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    senha = db.Column(db.String(300), nullable=False)
    idade = db.Column(db.Integer(), nullable=False)
    cpfCnpj = db.Column(db.String(30), nullable=False)
    endereco = db.relationship('Endereco', backref=db.backref('Usuario',   lazy=True), passive_deletes=True)
    livro = db.relationship('UsuarioTemLivro', backref=db.backref('Usuario',   lazy=True), passive_deletes=True)

    def __init__(self, nome, sobrenome, email, senha, idade, cpfCnpj):
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha = senha
        self.idade = idade
        self.cpfCnpj = cpfCnpj


class Livro(db.Model):
    __tablename__ = "Livro"
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(250), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    editora = db.Column(db.String(200), nullable=False)
    preco = db.Column(db.Float(), nullable=False)
    status = db.Column(db.Integer(), nullable=False)
    usuario = db.relationship('UsuarioTemLivro', backref=db.backref('Livro',   lazy=True), passive_deletes=True)

    def __init__(self, autor, titulo, editora, preco, status):
        self.autor = autor
        self.titulo = titulo
        self.editora = editora
        self.preco = preco
        self.status = status


class UsuarioTemLivro(db.Model):
    __tablename__ = "UsuarioTemLivro"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id', ondelete='CASCADE'), nullable=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('Livro.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, usuario, livro):
        self.usuario_id = usuario
        self.livro_id = livro


class Endereco(db.Model):
    __tablename__ = "Endereco"
    id = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(100), nullable=False)
    cidade = db.Column(db.String(150), nullable=False)
    bairro = db.Column(db.String(150), nullable=False)
    rua = db.Column(db.String(300), nullable=False)
    numero = db.Column(db.String(6), nullable=False)
    complemento = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longetude = db.Column(db.Float(), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, estado, cidade, bairro, rua, numero, complemento, latitude, longetude, usuario_id):
        self.estado = estado
        self.cidade = cidade
        self.bairro = bairro
        self.rua = rua
        self.numero = numero
        self.complemento = complemento
        self.latitude = latitude
        self.longetude = longetude
        self.usuario_id = usuario_id


class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "nome", "sobrenome","email", "idade", "cpfCnpj")

class LivrosSchema(ma.Schema):
    class Meta:
        fields = ("id", "autor", "titulo", "editora", "preco", "status")

class EnderecoSchema(ma.Schema):
    class Meta:
        fields = ("id", "estado", "cidade", "bairro", "rua", "numero", "complemento", "latitude", "longetude", "usuario_id")


class UsuarioTemLivroSchema(ma.Schema):
    class Meta:
        fields = ("id", "usuario_id", "livro_id")
