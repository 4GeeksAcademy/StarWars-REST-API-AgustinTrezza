import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character, Starship, PlanetsFavorites, CharactersFavorites, StarshipsFavorites

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

# Crear datos de prueba
@app.before_first_request
def create_hardcoded_data():
    if not User.query.filter_by(email="testuser@example.com").first():
        user = User(full_name="Test User", email="testuser@example.com", password="password")
        db.session.add(user)
        db.session.commit()
        print("Hardcoded user created")

    if not Planet.query.filter_by(name="Tatooine").first():
        planet = Planet(name="Tatooine", rotation_period="23", orbital_period="304", diameter="10465", climate="arid", terrain="desert")
        db.session.add(planet)
        db.session.commit()
        print("Hardcoded planet created")

    if not Character.query.filter_by(name="Luke").first():
        character = Character(name="Luke", last_name="Skywalker", height="172", mass="77", birth_year="19BBY")
        db.session.add(character)
        db.session.commit()
        print("Hardcoded character created")

    if not Starship.query.filter_by(name="Millennium Falcon").first():
        starship = Starship(name="Millennium Falcon", model="YT-1300 light freighter", manufacturer="Corellian Engineering Corporation", length="34.37", crew="4", passengers="6", consumables="2 months")
        db.session.add(starship)
        db.session.commit()
        print("Hardcoded starship created")

    # Crear favoritos de ejemplo
    user = User.query.filter_by(email="testuser@example.com").first()
    planet = Planet.query.filter_by(name="Tatooine").first()
    character = Character.query.filter_by(name="Luke").first()
    starship = Starship.query.filter_by(name="Millennium Falcon").first()

    if user and planet and not PlanetsFavorites.query.filter_by(user_id=user.id, planet_id=planet.id).first():
        favorite_planet = PlanetsFavorites(user_id=user.id, planet_id=planet.id)
        db.session.add(favorite_planet)
        db.session.commit()
        print("Hardcoded planet favorite created")

    if user and character and not CharactersFavorites.query.filter_by(user_id=user.id, character_id=character.id).first():
        favorite_character = CharactersFavorites(user_id=user.id, character_id=character.id)
        db.session.add(favorite_character)
        db.session.commit()
        print("Hardcoded character favorite created")

    if user and starship and not StarshipsFavorites.query.filter_by(user_id=user.id, starship_id=starship.id).first():
        favorite_starship = StarshipsFavorites(user_id=user.id, starship_id=starship.id)
        db.session.add(favorite_starship)
        db.session.commit()
        print("Hardcoded starship favorite created")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_all_people():
    people = Character.query.all()
    return jsonify([person.serialize() for person in people]), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_single_person(people_id):
    person = Character.query.get(people_id)
    if not person:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(person.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    planets_favorites = PlanetsFavorites.query.filter_by(user_id=user_id).all()
    characters_favorites = CharactersFavorites.query.filter_by(user_id=user_id).all()
    starships_favorites = StarshipsFavorites.query.filter_by(user_id=user_id).all()
    return jsonify({
        "planets": [fav.serialize() for fav in planets_favorites],
        "characters": [fav.serialize() for fav in characters_favorites],
        "starships": [fav.serialize() for fav in starships_favorites]
    }), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    new_favorite = PlanetsFavorites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    new_favorite = CharactersFavorites(user_id=user_id, character_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    favorite = PlanetsFavorites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID not provided"}), 400
    favorite = CharactersFavorites.query.filter_by(user_id=user_id, character_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
