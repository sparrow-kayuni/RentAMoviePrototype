from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import Config
from app.dashboard import dashboard_bp
from app.rental_txn import rental_txn_bp
from app.customers import customers_bp
from app.videos import videos_bp

rentamovie = Flask(__name__)
rentamovie.config.from_object(Config)

db = SQLAlchemy(rentamovie)
migrate = Migrate(rentamovie, db)

from app import routes
from app.dashboard import routes
from app.rental_txn import routes
from app.customers import routes
from app.videos import routes

rentamovie.register_blueprint(dashboard_bp, url_prefix='/dashboard')
rentamovie.register_blueprint(rental_txn_bp, url_prefix='/rental')
rentamovie.register_blueprint(customers_bp, url_prefix='/customers')
rentamovie.register_blueprint(videos_bp, url_prefix='/videos')