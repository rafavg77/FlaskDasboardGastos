class Config(object):
    """Base config, uses staging database server."""
    TESTING = False
    DEBUG = False
    
class ProductionConfig(Config):
    """Uses production database server."""
    SECRET_KEY = 'uahsdqweiodjhaskldhiwjouiweroiwef'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production_app.db'

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'mysecretkeysdsdasdwweede'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'testingsdhhdheje'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
