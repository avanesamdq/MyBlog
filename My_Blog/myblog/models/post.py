
from myblog import db
from datetime import datetime

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column( db.Integer, primary_key= True)
    author = db.Column( db.Integer, db.ForeignKey('users.id'), nullable = False )
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    im = db.Column(db.String(100), nullable = True)

    def __init__(self, author, title, body, im) -> None:
        self.author = author
        self.title = title
        self.body = body
        self.im = im

    def __repr__(self) -> str:

        return f'Post: {self.title}'

""" 
Construcción de los modelos.
Desde las vistas reutilizo los modelos y realizo la conexion, capturo la 
peticion del usuario y responder al usuario.
La carpeta "models" es un paquete lleva un archivo (__init__.py) para indicar 
que "models" es un paquete. 

"""
