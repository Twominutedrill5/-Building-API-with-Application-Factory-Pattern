class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Dahlia414!@127.0.0.1/mechanic_connection'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:Dahlia414!@127.0.0.1/mechanic_connection'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300