class Config(object):
    DEBUG = False
    TESTING = False
    
class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'super_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../seek_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'super_secret_salt'
    SECURITY_REGISTERABLE = True
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_LEY = 'super_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../seek_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'test-secret-key'
    SECURITY_PASSWORD_SALT = 'test_secret_salt'
    SECURITY_REGISTERABLE = True