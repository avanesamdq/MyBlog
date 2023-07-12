class Config:
    DEBUG = True
    TESTING = True

    #Config de base de datos
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/blog_db'

# Clase modo de producccion. 

# Heredar de la clase (config) toda la configuracion q tiene por defecto
class ProductionConfig(Config):
    DEBUG = False

# Clase modo de desarrollo
class DevelopmentConfig(Config): 
    # La secretkey(key) nos va a pedir cuando nosotros estemos trabajando 
    # al momento de rendirizar un mensaje de error o un mensaje de seguridad tenemos que tener esta key.
    DEBUG = True
    SECRET_KEY = 'dev'
    # En modo de desarrollo tambien vamos a poder testear 
    TESTING = True
    