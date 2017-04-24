
class Config(object):
    """
    Configuration base, for all environments.
    """
    DEBUG = False
    DATABASE_URI = 'sqlite:///application.db'
    SECRET_KEY = "LKHSDNIOUTY&*(^87bv6*&BGSUYDS"
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    PORT = 5010
    HOST = '127.0.0.1'

    URL = 'http://lala.com'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///application.db'

