from app import create_app
from backend.models import db, Role, User, Course
from backend.sec import datastore
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash

# Create the Flask application context
app = create_app()

with app.app_context():
    # Create roles if they do not exist
    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        admin_role = Role(name='admin', description='User is an admin')
        db.session.add(admin_role)

    creator_role = Role.query.filter_by(name='creator').first()
    if not creator_role:
        creator_role = Role(name='creator', description='User is a creator')
        db.session.add(creator_role)

    user_role = Role.query.filter_by(name='user').first()
    if not user_role:
        user_role = Role(name='user', description='Regular user')
        db.session.add(user_role)

    # Commit roles to the database
    db.session.commit()

    # Create the 'admin' user if not exist
    admin_user = User.query.filter_by(email='admin@email.com').first()
    if not admin_user:
        admin_user = datastore.create_user(email='admin@email.com', username='admin', password=generate_password_hash('admin'), active=True, roles=[admin_role])
        db.session.add(admin_user)

    # Create the 'creator' user if not exist
    creator_user = User.query.filter_by(email='creator@email.com').first()
    if not creator_user:
        creator_user = datastore.create_user(email='creator@email.com', username='creator', password=generate_password_hash('creator'), active=False, roles=[creator_role])
        db.session.add(creator_user)

    # Create the 'user' if not exist
    regular_user = User.query.filter_by(email='user@email.com').first()
    if not regular_user:
        regular_user = datastore.create_user(email='user@email.com', username='user', password=generate_password_hash('user'), active=True, roles=[user_role])
        db.session.add(regular_user)

    # Commit all changes to the database
    db.session.commit()
