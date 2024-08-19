class Config(object):
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../seek_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'super-secret-salt'
    SECURITY_REGISTERABLE = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = 'super-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../seek_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    SECURITY_PASSWORD_SALT = 'test-secret-salt'
    SECURITY_REGISTERABLE = True
