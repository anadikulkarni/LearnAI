import os
import sys
import time
import json
import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, parent_dir)

from app import create_app
from backend.models import db, Assignment, Role
from backend.sec import datastore
from config import TestingConfig
from datetime import datetime

RESULTS_FILE = 'assignment_test_results.json'

now = datetime.now()  # Gets the current date and time
current_date = now.date()  # Extracts the date part

def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, 'r') as file:
            return json.load(file)
    return []

def save_results(results):
    with open(RESULTS_FILE, 'w') as file:
        json.dump(results, file, indent=4)
    print(f"Data saved to {RESULTS_FILE}")

class TestAssignmentResource(TestCase):
    def create_app(self):
        return create_app(TestingConfig)

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create roles and a test user
        admin_role = Role(name='admin', description='Admin role')
        instructor_role = Role(name='instructor', description='Instructor role')
        db.session.add(admin_role)
        db.session.add(instructor_role)
        db.session.commit()

        self.admin_user = datastore.create_user(
            email='admin@example.com', 
            username='admin', 
            password=generate_password_hash('admin'), 
            active=True, 
            roles=[admin_role]
        )
        db.session.add(self.admin_user)
        db.session.commit()

        self.headers = {'Authorization': 'Bearer ' + self.get_token(self.admin_user.email, 'admin')}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_token(self, email, password):
        response = self.client.post('/api/login', json={'email': email, 'password': password})
        return response.get_json()['token']

    def log_test(self, endpoint, response, start_time):
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

    def test_get_all_assignments(self):
        start_time = time.time()
        response = self.client.get('/api/assignments')
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        self.log_test('/api/assignments', response, start_time)

    def test_get_assignment_by_id(self):
        start_time = time.time()
        assignment = Assignment(title='Test Assignment', description='Description', created_at=datetime.now())
        db.session.add(assignment)
        db.session.commit()

        response = self.client.get(f'/api/assignments/{assignment.id}')
        assert response.status_code == 200
        assert response.get_json()['title'] == 'Test Assignment'
        self.log_test(f'/api/assignments/{assignment.id}', response, start_time)

    def test_create_assignment(self):
        start_time = time.time()
        data = {
            'title': 'New Assignment',
            'description': 'Assignment description',
        }
        response = self.client.post('/api/assignments', json=data, headers=self.headers)
        assert response.status_code == 201
        assert response.get_json()['title'] == 'New Assignment'
        self.log_test('/api/assignments', response, start_time)

    def test_update_assignment(self):
        start_time = time.time()
        assignment = Assignment(title='Old Assignment', description='Old description')
        db.session.add(assignment)
        db.session.commit()

        data = {
            'title': 'Updated Assignment',
            'description': 'Updated description',
        }
        response = self.client.put(f'/api/assignments/{assignment.id}', json=data, headers=self.headers)
        assert response.status_code == 200
        assert response.get_json()['title'] == 'Updated Assignment'
        self.log_test(f'/api/assignments/{assignment.id}', response, start_time)

    def test_delete_assignment(self):
        start_time = time.time()
        assignment = Assignment(title='Test Assignment', description='Description', created_at=datetime.now())
        db.session.add(assignment)
        db.session.commit()

        response = self.client.delete(f'/api/assignments/{assignment.id}', headers=self.headers)
        assert response.status_code == 204
        assert Assignment.query.get(assignment.id) is None
        self.log_test(f'/api/assignments/{assignment.id}', response, start_time)
