import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    SECRET_KEY = os.urandom (24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'ai.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_TEARDOWN = True


    @staticmethod
    def init_app(app):
        pass


