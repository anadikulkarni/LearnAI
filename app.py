import logging
from flask import Flask
from flask_security import Security
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import db, User
from config import DevelopmentConfig
from backend.api_declare import create_api
from backend.sec import datastore
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    
    api = create_api(app)
    app.security = Security(app, datastore)
    
    with app.app_context():
        import backend.views
        db.create_all()  # Create tables here

    return app

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

# Database connection
DATABASE_URL = DevelopmentConfig.SQLALCHEMY_DATABASE_URI
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)