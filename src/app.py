"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Personajes, Planetas, User, Favoritos
from sqlalchemy import select 

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#obtener todos los personajes 
@app.route('/personajes', methods=['GET'])
def todos_los_personajes():

    data = db.session.scalars(select(Personajes)).all()
    results = list(map(lambda Personajes: Personajes.serialize(),data))
    

    response_body = {
        "msg": "Hello, this is your GET /user response ", 
        "results":results
    }

    return jsonify(response_body), 200

# obtener un solo personaje
@app.route('/personajes/<int:id>', methods=['GET'])
def solo_un_personaje(id):
    
 try: 

    personaje = db.session.execute(select(Personajes).filter_by(id=id)).scalar_one()
    
    
    

    response_body = {
        "msg": "Hello, this is your GET /personaje response ", 
        "results":personaje.serialize()
    }

    return jsonify(response_body), 200

 except: 

    return jsonify({"msg":"user not exist"}), 404
 

#obtener todos los planetas
@app.route('/planetas', methods=['GET'])
def todos_los_planetas():

    data = db.session.scalars(select(Planetas)).all()
    results = list(map(lambda Planetas: Planetas.serialize(),data))
    

    response_body = {
        "msg": "Hello, this is your GET /todos los planetas response ", 
        "results":results
    }

    return jsonify(response_body), 200 


# obtener un solo planeta
@app.route('/planetas/<int:id>', methods=['GET'])
def solo_un_planeta(id):
    
 try: 

    planeta = db.session.execute(select(Planetas).filter_by(id=id)).scalar_one()
    
    
    

    response_body = {
        "msg": "Hello, this is your GET /planetaresponse ", 
        "results":planeta.serialize()
    }

    return jsonify(response_body), 200

 except: 

    return jsonify({"msg":"planeta not exist"}), 404
 
 
#obtener todos los usuarios
@app.route('/user', methods=['GET'])
def todos_los_usuarios():

    data = db.session.scalars(select(User)).all()
    results = list(map(lambda User: User.serialize(),data))
    
    

    response_body = {
        "msg": "Hello, this is your GET /todos los usuarios response ", 
        "results":results
    }

    return jsonify(response_body), 200  

#obtener todos los favoritos 
@app.route('/favoritos', methods=['GET'])
def todos_los_favoritos():

    data = db.session.scalars(select(Favoritos)).all()
    results = list(map(lambda Favoritos: Favoritos.serialize(),data))
    

    response_body = {
        "msg": "Hello, this is your GET /todos los favoritos ", 
        "results":results
    }

    return jsonify(response_body), 200  

#obtener el planeta favorito de un usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def añadir_favorito_planeta(planet_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
     return jsonify({"msg": "No User send "}), 404

    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    
    if not user:
     return jsonify({"error": "Usuario no encontrado"}), 404

    new_favorito = Favoritos(user_id=user.id,planeta_id=planet_id)
    db.session.add(new_favorito)
    db.session.commit()

    response_body = {
        "msg":"planeta favorito agregado"
    }

    return jsonify(response_body), 200


#obtener el personaje favorito de un usuario
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def añadir_favorito_personaje(people_id):
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
     return jsonify({"msg": "No User send "}), 404

    user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar()
    
    if not user:
     return jsonify({"error": "Usuario no encontrado"}), 404
       

    new_favorito = Favoritos(user_id=user_id,personajes_id=people_id)
    db.session.add(new_favorito)
    db.session.commit()

    response_body = {
        "msg":"personaje favorito agregado"
    }

    return jsonify(response_body), 200


    ##### DELETE planeta favorito
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    # hacer filtrado
    buscar_planetafavorito_borrar = Favoritos(user_id=user.id,planeta_id=planet_id)
    db.session.delete(buscar_planetafavorito_borrar)
    db.session.commit()

    response_body = {
        "msg":"planeta favorito del usuario deleted"
    }

    return jsonify(response_body), 200


##### DELETE personaje favorito
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_user(people_id):

    user = db.session.execute(db.select(User).filter_by(id=id)).scalar_one()
    # hacer filtrado
    buscar_personajefavorito_borrar = Favoritos(user_id=user.id,personajes_id=people_id)
    db.session.delete(buscar_personajefavorito_borrar)
    db.session.commit()

    response_body = {
        "msg":"planeta favorito del usuario deleted"
    }

    return jsonify(response_body), 200
 
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)





