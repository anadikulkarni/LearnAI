from flask import Flask
from flask_security import Security
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = DevelopmentConfig

