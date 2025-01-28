from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import Integer, String, Boolean, ForeignKey 

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String(120), nullable=False)
    password = mapped_column(String(80))
    is_active = mapped_column(Boolean)
    nombre = mapped_column(String(80))
    # aqui estoy accediendo desde el objeto favoritos puedo 
    favoritos = relationship("Favoritos", back_populates="user") 
    


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Personajes(db.Model):
    __tablename__ = "personaje"

    id = mapped_column(Integer, primary_key=True)
    altura = mapped_column(String(120), nullable=False)
    color_de_pelo = mapped_column(String(80))
    color_de_ojos = mapped_column(String(80))
    genero =  mapped_column(String(80))   
    favoritos = relationship("Favoritos", back_populates ="personaje")

    def serialize(self):
        return {
            "id": self.id,
            "altura": self.altura,
            "color_de_pelo": self.color_de_pelo,
            "color_de_ojos": self.color_de_ojos,
            "genero": self.genero,
        }

class Planetas(db.Model):
    __tablename__ = "planetas"

    id = mapped_column(Integer, primary_key=True)
    poblacion = mapped_column(String(120), nullable=False)
    terreno = mapped_column(String(80), nullable = False)
    admosfera = mapped_column(String(80), nullable = False)
    favoritos = relationship("Favoritos", back_populates = "planeta")

    def serialize(self):
        return {
            "id": self.id,
            "poblacion": self.poblacion,
            "terreno": self.terreno,
            "admosfera": self.admosfera
            
        }

class Favoritos(db.Model):
    __tablename__ = "favoritos"

    id = mapped_column(Integer, primary_key=True) 

    planeta_id = mapped_column(Integer, ForeignKey("planetas.id"), nullable=True) 
    planeta =  relationship ("Planetas", back_populates = "favoritos")

    personajes_id = mapped_column(Integer, ForeignKey("personaje.id"), nullable=True)
    personaje = relationship ("Personajes", back_populates = "favoritos")

    user_id = mapped_column(Integer, ForeignKey("user.id"), nullable = False)
    user = relationship("User", back_populates = "favoritos")
