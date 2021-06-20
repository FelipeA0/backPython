from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json

app = Flask(__name__)

app.secret_key = 'myawesomesecretkey'

app.config["MONGO_URI"] = "mongodb+srv://FelipeA0:12345@infinafilms.kotmx.mongodb.net/Infinafilms?retryWrites=true&w=majority"
mongo = PyMongo(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World! jijiji</p>"

@app.route("/getUsuarios", methods=['GET'])
def get_users():
    usuarios = mongo.db.usuarios.find()
    response = json_util.dumps(usuarios)
    return Response(response, mimetype='application/json')

@app.route('/insertarUsuario', methods=['POST'])
def crear_usuario():
    request.get_json(force=True)
    nombre = request.json['nombre']
    contraseña = request.json['contraseña']
    rol = request.json['rol']

    if nombre and contraseña and rol:
        id = mongo.db.usuarios.insert(
            {'nombre': nombre, 'contraseña': contraseña, 'rol': rol}
        )
        response = jsonify({
            '_id': str(id),
            'nombre': nombre,
            'contraseña': contraseña,
            'rol': rol
        })
        response.status_code = 201
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run(debug = True)