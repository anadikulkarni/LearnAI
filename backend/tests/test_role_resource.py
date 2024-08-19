import json
import pytest
from flask_testing import TestCase
from app import create_app
from backend.models import db, Role
from config import TestingConfig

class TestRoleResource(TestCase):

    @classmethod
    def create_app(cls):
        """Create and return the Flask app instance for testing."""
        return create_app(config_class=TestingConfig)

    def setUp(self):
        """Set up the test case environment."""
        # Create tables and add sample data
        db.create_all()
        self._create_sample_role()

    def tearDown(self):
        """Tear down the test case environment."""
        db.session.remove()
        db.drop_all()

    def _create_sample_role(self):
        """Helper method to create a sample role."""
        self.role = Role(name='admin', description='Administrator role')
        db.session.add(self.role)
        db.session.commit()

    def test_get_all_roles(self):
        """Test retrieving all roles."""
        response = self.client.get('/api/roles')
        self.assertStatus(response, 200, "Expected status code 200 for retrieving all roles.")
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'admin')

    def test_get_role_by_id(self):
        """Test retrieving a role by ID."""
        response = self.client.get(f'/api/roles/{self.role.id}')
        self.assertStatus(response, 200, "Expected status code 200 for retrieving role by ID.")
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'admin')

    def test_get_role_not_found(self):
        """Test retrieving a non-existent role."""
        response = self.client.get('/api/roles/9999')
        self.assertStatus(response, 404, "Expected status code 404 for non-existent role.")

    def test_create_role(self):
        """Test creating a new role."""
        new_role = {
            'name': 'editor',
            'description': 'Editor role'
        }
        response = self.client.post('/api/roles', json=new_role)
        self.assertStatus(response, 201, "Expected status code 201 for creating a new role.")
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'editor')

    def test_update_role(self):
        """Test updating an existing role."""
        updated_role = {
            'name': 'superadmin',
            'description': 'Updated description'
        }
        response = self.client.put(f'/api/roles/{self.role.id}', json=updated_role)
        self.assertStatus(response, 200, "Expected status code 200 for updating role.")
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'superadmin')

    def test_update_role_not_found(self):
        """Test updating a non-existent role."""
        updated_role = {
            'name': 'superadmin',
            'description': 'Updated description'
        }
        response = self.client.put('/api/roles/9999', json=updated_role)
        self.assertStatus(response, 404, "Expected status code 404 for non-existent role.")

    def test_delete_role(self):
        """Test deleting an existing role."""
        response = self.client.delete(f'/api/roles/{self.role.id}')
        self.assertStatus(response, 204, "Expected status code 204 for deleting role.")
        # Verify that the role has been deleted
        response = self.client.get('/api/roles')
        self.assertStatus(response, 200, "Expected status code 200 for retrieving all roles after deletion.")
        data = json.loads(response.data)
        self.assertEqual(len(data), 0)

    def test_delete_role_not_found(self):
        """Test deleting a non-existent role."""
        response = self.client.delete('/api/roles/9999')
        self.assertStatus(response, 404, "Expected status code 404 for non-existent role.")

if __name__ == '__main__':
    pytest.main()
