import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATION =False
    
    @staticmethod
    def init_app(app):
        pass
    
class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URI")
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI") 

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DATABASE_URI") 
    
config = {
    'development': DevelopmentConfig,
    'testing' : TestingConfig,
    'production' : ProductionConfig,
}

