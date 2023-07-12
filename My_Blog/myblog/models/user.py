from myblog import db

# Se crea una clase y se convierte en un modelo de base de datos.

class User(db.Model): # La clase hereda del modelo de SQLAlchemy, con esto ya es un modelo.
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(50))
    password = db.Column(db.Text)

    # Para luego reutilizar esta clase se crea un constructor. 

    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    # Luego para representar como se va a mostrar este objeto tambien podemos usar en este caso
    # el metodo __repr__ el cual va a devolver un string

    def __repr__(self) -> str:
        return f'User: {self.username}'


""" 
Si colocamos o pasamos algunos atributos en la base de datos, lo va a tomar 
o lo va a colocar esta clase como un modelo y el nombre de la tabla lo va a colocar 
con nombre "user" en pura minuscula. Si queremos modificar el nombre de la tabla 
normalmente en bd se coloca en plural. Entonces colocamos __tablename__ y este va 
a ser igual a 'users' en plural.
"""