import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config (object):
    SECRET_KEY = os.environ.get('SECRET KEY') or 'secreteynoonecanguess'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE URL') or \
        'sqlite:///' + os.path.join(basedir, 'rent_a_movie.db')
    
    SQLACHEMY_TRACK_MODIFICATIONS = False