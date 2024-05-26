from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.full_name

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
        }

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    rotation_period = db.Column(db.String(250))
    orbital_period = db.Column(db.String(250))
    diameter = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    terrain = db.Column(db.String(250))

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250))
    height = db.Column(db.String(250))
    mass = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "height": self.height,
            "mass": self.mass,
            "birth_year": self.birth_year,
        }

class Starship(db.Model):
    __tablename__ = 'starships'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    length = db.Column(db.String(250))
    crew = db.Column(db.String(250))
    passengers = db.Column(db.String(250))
    consumables = db.Column(db.String(250))

    def __repr__(self):
        return '<Starship %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "consumables": self.consumables,
        }

class PlanetsFavorites(db.Model):
    __tablename__ = 'planets_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.relationship(User, backref=db.backref('planets_favorites', lazy=True))
    planet = db.relationship(Planet, backref=db.backref('planets_favorites', lazy=True))

    def __repr__(self):
        return '<PlanetsFavorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

class CharactersFavorites(db.Model):
    __tablename__ = 'characters_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user = db.relationship(User, backref=db.backref('characters_favorites', lazy=True))
    character = db.relationship(Character, backref=db.backref('characters_favorites', lazy=True))

    def __repr__(self):
        return '<CharactersFavorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }

class StarshipsFavorites(db.Model):
    __tablename__ = 'starships_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    starship_id = db.Column(db.Integer, db.ForeignKey('starships.id'))
    user = db.relationship(User, backref=db.backref('starships_favorites', lazy=True))
    starship = db.relationship(Starship, backref=db.backref('starships_favorites', lazy=True))

    def __repr__(self):
        return '<StarshipsFavorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
        }
