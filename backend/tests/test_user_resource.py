import json
import pytest
from flask_testing import TestCase
from werkzeug.security import generate_password_hash
from app import create_app
from backend.models import db, User, Role, RolesUsers
from backend.sec import datastore
from config import TestingConfig

class TestUserResource(TestCase):

    @classmethod
    def create_app(cls):
        """Create and return the Flask app instance for testing."""
        return create_app(config_class=TestingConfig)

    def setUp(self):
        """Set up the test case environment."""
        db.create_all()
        self._create_sample_roles()  # Create roles up to ID 3
        self._create_sample_user()   # Create a sample user with role ID 1

    def tearDown(self):
        """Tear down the test case environment."""
        db.session.remove()
        db.drop_all()

    def _create_sample_roles(self):
        """Helper method to create sample roles up to ID 3."""
        roles = [
            {'name': 'admin', 'description': 'Administrator role'},
            {'name': 'moderator', 'description': 'Moderator role'},
            {'name': 'user', 'description': 'Regular user role'}
        ]
        
        for role in roles:
            existing_role = Role.query.filter_by(name=role['name']).first()
            if not existing_role:
                new_role = Role(name=role['name'], description=role['description'])
                db.session.add(new_role)
        
        db.session.commit()

    def _create_sample_user(self):
        """Helper method to create a sample user."""
        self.user = datastore.create_user(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('password'),
            active=True
        )
        db.session.add(self.user)
        db.session.commit()

        # Assign the sample role to the sample user
        role_user = RolesUsers(user_id=self.user.id, role_id=1)  # Role ID 1 (admin)
        db.session.add(role_user)
        db.session.commit()

    def test_create_user(self):
        """Test creating a new user with role_id 3."""
        new_user = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'role_id': 3  # Assign the role with ID 3 (user)
        }
        response = self.client.post('/api/users', json=new_user)
        self.assertStatus(response, 201, "Expected status code 201 for creating a new user.")
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'newuser')
        self.assertEqual(int(data['role_id']), 3)
        self.assertEqual(data['role_name'], 'user')

    def test_create_user_with_invalid_role_id(self):
        """Test creating a user with an invalid role_id."""
        new_user = {
            'username': 'anotheruser',
            'email': 'another@example.com',
            'password': 'anotherpassword',
            'role_id': 1  # Invalid role_id
        }
        response = self.client.post('/api/users', json=new_user)
        self.assertStatus(response, 400, "Expected status code 400 for invalid role_id.")
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Invalid role_id. Only 3 or 5 are allowed')

    def test_get_all_users(self):
        """Test retrieving all users."""
        response = self.client.get('/api/users')
        self.assertStatus(response, 200, "Expected status code 200 for retrieving all users.")
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], 'testuser')
        self.assertEqual(int(data[0]['role_id']), 1)
        self.assertEqual(data[0]['role_name'], 'admin')

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        response = self.client.get(f'/api/users/{self.user.id}')
        self.assertStatus(response, 200, "Expected status code 200 for retrieving user by ID.")
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'testuser')
        self.assertEqual(int(data['role_id']), 1)
        self.assertEqual(data['role_name'], 'admin')

    def test_update_user(self):
        """Test updating an existing user."""
        updated_user = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'role_id': 3  # Update to role ID 3 (user)
        }
        response = self.client.put(f'/api/users/{self.user.id}', json=updated_user)
        self.assertStatus(response, 200, "Expected status code 200 for updating user.")
        data = json.loads(response.data)
        self.assertEqual(data['username'], 'updateduser')
        self.assertEqual(data['email'], 'updated@example.com')
        self.assertEqual(int(data['role_id']), 3)
        self.assertEqual(data['role_name'], 'user')

    def test_delete_user(self):
        """Test deleting a user."""
        response = self.client.delete(f'/api/users/{self.user.id}')
        self.assertStatus(response, 204, "Expected status code 204 for deleting user.")
        # Verify that the user has been deleted
        response = self.client.get('/api/users')
        self.assertStatus(response, 200, "Expected status code 200 for retrieving all users after deletion.")
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

if __name__ == '__main__':
    pytest.main()
