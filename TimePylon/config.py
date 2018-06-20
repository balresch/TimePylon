from os import path

basedir = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = '\x14\xcb\xfd\xa5\xa2m\xb0\xf7\xd0\xaf#\x02\xfd\x92\xa9\xd0"\xd6\x81cY\x0f\\\xaa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "TimePylon.db")

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "data-test.sqlite")

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "TimePylon.db")

config_by_name = dict(
    dev = DevelopmentConfig,
    test = TestingConfig,
    prod = ProductionConfig
)
