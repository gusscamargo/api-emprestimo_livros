from json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request

from model import Endereco, EnderecoSchema

from geopy.geocoders import Nominatim

app = Flask(__name__)
db = SQLAlchemy(app)

endereco_schema = EnderecoSchema()
enderecos_schema = EnderecoSchema(many=True)


#(self, estado, cidade, bairro, rua, numero, complemento, latitude, longetude)
class BancoEndereco:
    def addEndereco(request):
        localizacaoEngine = Nominatim(user_agent="myGeocoder")
        gps = localizacaoEngine.geocode("{:}, {:}, {:}, {:}, Brazil".format(request.json['rua'], request.json['bairro'], request.json['cidade'], request.json['estado']))

        novoEndereco = Endereco(
            request.json['estado'],
            request.json['cidade'],
            request.json['bairro'],
            request.json['rua'],
            request.json['numero'],
            request.json['complemento'],
            gps.latitude,
            gps.longitude,
            request.json["usuario_id"]
        )

        db.session.add(novoEndereco)
        db.session.commit()
        db.session.close()

        return jsonify({"status": "successful"})

    def getEnderecoUsuario(id):
        enderecos = Endereco.query.filter_by(usuario_id = id).all()

        resultado = enderecos_schema.dump(enderecos)

        return jsonify(resultado)
