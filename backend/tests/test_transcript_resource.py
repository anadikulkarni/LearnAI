import os
import sys
import json
import time
import pytest
from flask_testing import TestCase

from werkzeug.security import generate_password_hash
from app import create_app
from backend.models import db, LectureTranscript, Course, Category, Role, User
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

class TestTranscriptResource:

    @classmethod
    def setup_class(cls):
        cls.app = create_app(TestingConfig)
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Set up test data
        category = Category(name='Programming')
        db.session.add(category)

        admin_role = Role(name='admin', description='Can create and manage courses')
        db.session.add(admin_role)
        db.session.commit()
        
        # Create a test user with admin role
        admin_user = datastore.create_user(email='admin@email.com', username='admin', password=generate_password_hash('admin'), active=True, roles=[admin_role])
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

    def test_post_transcript_success(self):
        start_time = time.time()
        data = {
            'video_id': 'ZU1oJJq_Wh0',
            'course_id': 1
        }
        response = self.client.post('/api/transcript', json=data)
        assert response.status_code == 201
        assert 'Transcript added successfully' in response.get_json()['message']
        self.log_test('/api/transcript', response, start_time)

    def test_post_transcript_missing_fields(self):
        start_time = time.time()
        data = {
            'video_id': 'abc123'
            # Missing course_id
        }
        response = self.client.post('/api/transcript', json=data)
        assert response.status_code == 400
        assert response.get_json()['error'] == "video_id and course_id are required"
        self.log_test('/api/transcript', response, start_time)

    def test_get_transcript_success(self):
        start_time = time.time()
        # Create a transcript first
        new_transcript = LectureTranscript(content='This is the transcript text', course_id=1)
        db.session.add(new_transcript)
        db.session.commit()

        response = self.client.get(f'/api/transcript/{new_transcript.content}')
        assert response.status_code == 200
        assert response.get_json()['transcript'] == 'This is the transcript text'
        self.log_test(f'/api/transcript/{new_transcript.content}', response, start_time)

    def test_get_transcript_not_found(self):
        start_time = time.time()
        response = self.client.get('/api/transcript/unknown_video_id')
        assert response.status_code == 500
        assert 'error' in response.get_json()
        self.log_test('/api/transcript/unknown_video_id', response, start_time)

    def test_put_transcript_success(self):
        start_time = time.time()
        # Create a transcript first
        new_transcript = LectureTranscript(content='Original transcript text', course_id=1)
        db.session.add(new_transcript)
        db.session.commit()

        updated_data = {
            'content': 'Updated transcript text',
            'course_id': 2
        }
        response = self.client.put(f'/api/transcript/{new_transcript.content}', json=updated_data)
        assert response.status_code == 200
        assert 'Transcript updated successfully' in response.get_json()['message']
        assert response.get_json()['transcript'] == 'Updated transcript text'
        self.log_test(f'/api/transcript/{new_transcript.content}', response, start_time)

    def test_put_transcript_not_found(self):
        start_time = time.time()
        updated_data = {
            'content': 'Updated transcript text',
            'course_id': 2
        }
        response = self.client.put('/api/transcript/unknown_video_id', json=updated_data)
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Transcript not found'
        self.log_test('/api/transcript/unknown_video_id', response, start_time)

    def test_delete_transcript_success(self):
        start_time = time.time()
        # Create a transcript first
        new_transcript = LectureTranscript(content='Transcript text to delete', course_id=1)
        db.session.add(new_transcript)
        db.session.commit()

        response = self.client.delete(f'/api/transcript/{new_transcript.content}')
        assert response.status_code == 200
        assert response.get_json()['message'] == 'Transcript deleted successfully'
        assert LectureTranscript.query.get(new_transcript.id) is None
        self.log_test(f'/api/transcript/{new_transcript.content}', response, start_time)

    def test_delete_transcript_not_found(self):
        start_time = time.time()
        response = self.client.delete('/api/transcript/unknown_video_id')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Transcript not found'
        self.log_test('/api/transcript/unknown_video_id', response, start_time)
