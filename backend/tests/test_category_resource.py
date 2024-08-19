import os
import sys
import json
import time
import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, parent_dir)

print(f"Current directory: {current_dir}")
print(f"Parent directory added to path: {parent_dir}")
print(f"sys.path: {sys.path}")

# Import create_app from app.py
from app import create_app
from backend.models import db, Category, Role, User
from backend.sec import datastore
from config import TestingConfig

# Define the path for the Results JSON file
RESULTS_FILE = 'test_results.json'

def load_results():
    """Load existing results from the JSON file."""
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_results(results):
    """Save results to the JSON file."""
    with open(RESULTS_FILE, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Data saved to {RESULTS_FILE}")


class TestCategoryResource:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        db.create_all()

        # Create test roles
        admin_role = Role(name='admin', description='Can create and manage categories')
        db.session.add(admin_role)
        db.session.commit()
        
        # Create test users
        admin_user = datastore.create_user(email='admin@example.com', username='admin', password=generate_password_hash('admin'), active=True, roles=[admin_role])
        db.session.add(admin_user)
        db.session.commit()

    @classmethod
    def teardown_class(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    def log_test(self, endpoint, response, start_time):
        """Log test details to a JSON file."""
        elapsed_time = time.time() - start_time
        results = load_results()
        result = {
            'endpoint': endpoint,
            'request_url': response.request.url,
            'response_status': response.status_code,
            'response_data': response.data.decode('utf-8'),
            'time_taken': round(elapsed_time, 2)
        }
        results.append(result)
        save_results(results)


    def test_get_categories(self):
        start_time = time.time()
        response = self.client.get('/api/categories')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        self.log_test('/api/categories', response, start_time)

    def test_get_category_by_id(self):
        # Create a category first
        start_time = time.time()
        category = Category(name='Linux')
        db.session.add(category)
        db.session.commit()

        response = self.client.get(f'/api/categories/{category.id}')
        assert response.status_code == 200
        assert response.get_json()['name'] == 'Linux'
        self.log_test(f'/api/categories/{category.id}', response, start_time)

    def test_post_category(self):
        start_time = time.time()
        data = {
            "name": "Git basics"
        }
        response = self.client.post('/api/categories', json=data)
        assert response.status_code == 201
        assert response.get_json()['name'] == 'Git basics'
        self.log_test('/api/categories', response, start_time)

    def test_put_category(self):
        # Create a category first
        start_time = time.time()
        category = Category(name='Diploma')
        db.session.add(category)
        db.session.commit()

        data = {
            "name": "Updated Degree Category",
            "description": "Updated description"
        }
        response = self.client.put(f'/api/categories/{category.id}', json=data)
        assert response.status_code == 200
        assert response.get_json()['name'] == 'Updated Degree Category'
        self.log_test(f'/api/categories/{category.id}', response, start_time)

    def test_delete_category(self):
        # Create a category first
        start_time = time.time()
        category = Category(name='Category to delete')
        db.session.add(category)
        db.session.commit()

        response = self.client.delete(f'/api/categories/{category.id}')
        assert response.status_code == 204
        self.log_test(f'/api/categories/{category.id}', response, start_time)
