from flask import Flask
from .models import db
from .routes import main_bp
import os

def create_app():
    """Application factory to create and configure the Flask app."""
    
    app = Flask(__name__)
    
    # Configure the app
    # It will look for the database in the main project folder
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    database_path = os.path.join(project_dir, 'users.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Register the blueprint from routes.py
    app.register_blueprint(main_bp)

    return app