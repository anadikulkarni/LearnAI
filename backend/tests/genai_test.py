import os
import sys
import json
import time
import pytest
from flask_testing import TestCase

# Adjust sys.path to include the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '../../'))
sys.path.insert(0, parent_dir)

print(f"Current directory: {current_dir}")
print(f"Parent directory added to path: {parent_dir}")
print(f"sys.path: {sys.path}")

# Import create_app from app.py
from app import create_app
from backend.models import db
from config import TestingConfig

# Define the path for the JSON file
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

class TestGenAIResources(TestCase):

    @classmethod
    def create_app(cls):
        """Create and return the Flask app instance for testing."""
        return create_app(config_class=TestingConfig)

    def setUp(self):
        """Set up the test case environment."""
        db.create_all()

    def tearDown(self):
        """Tear down the test case environment."""
        db.session.remove()
        db.drop_all()

    def log_test(self, endpoint, response, data, start_time):
        """Log test details to a JSON file."""
        elapsed_time = time.time() - start_time
        results = load_results()
        result = {
            'endpoint': endpoint,
            'request_data': data,
            'response_status': response.status_code,
            'response_data': response.data.decode('utf-8'),
            'time_taken': round(elapsed_time, 2)
        }
        results.append(result)
        save_results(results)

    def test_summarize_lecture(self):
        start_time = time.time()
        response = self.client.post('/api/llm/summary', 
                                    data=json.dumps({'transcript': 'Lecture transcript text'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('summary', data)
        self.log_test('/api/llm/summary', response, {'transcript': 'Lecture transcript text'}, start_time)

    def test_chatbot(self):
        start_time = time.time()
        response = self.client.post('/api/llm/chatbot', 
                                    data=json.dumps({'query': 'What is Python?'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('answer', data)
        self.log_test('/api/llm/chatbot', response, {'query': 'What is Python?'}, start_time)

    def test_feedback(self):
        start_time = time.time()
        response = self.client.post('/api/llm/feedback', 
                                    data=json.dumps({'code': "print(x)", 'error': "NameError: name 'x' is not defined"}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('feedback', data)
        self.log_test('/api/llm/feedback', response, {'code': "print(x)", 'error': "NameError: name 'x' is not defined"}, start_time)

    def test_quiz(self):
        start_time = time.time()
        response = self.client.post('/api/llm/quiz', 
                                    data=json.dumps({'topic': 'Machine Learning'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('questions', data)
        self.log_test('/api/llm/quiz', response, {'topic': 'Machine Learning'}, start_time)

    def test_translate(self):
        start_time = time.time()
        response = self.client.post('/api/llm/translate', 
                                    data=json.dumps({'transcript': 'Lecture content', 'language': 'French'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('translation', data)
        self.log_test('/api/llm/translate', response, {'transcript': 'Lecture content', 'language': 'French'}, start_time)

    def test_analyze_code(self):
        start_time = time.time()
        response = self.client.post('/api/llm/analyze_code', 
                                    data=json.dumps({'code': "def foo(): pass"}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('analysis', data)
        self.log_test('/api/llm/analyze_code', response, {'code': "def foo(): pass"}, start_time)

    def test_recommend_courses(self):
        start_time = time.time()

        # Ensure application context is correct
        with self.app.app_context():
            print("Application context:", self.app.app_context())
        
        # Print route information to check if it's registered
        print("Registered routes:", self.app.url_map)

        # Send POST request to the endpoint
        response = self.client.post('/api/llm/recommend_courses', 
                                    data=json.dumps({'user_id': 1}),
                                    content_type='application/json')

        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('recommendations', data)
        self.log_test('/api/llm/recommend_courses', response,{'user_id': 1}, start_time)


    def test_highlight_segments(self):
        start_time = time.time()
        response = self.client.post('/api/llm/highlight_segments', 
                                    data=json.dumps({'video_content': 'Lecture video text'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('highlights', data)
        self.log_test('/api/llm/highlight_segments', response, {'video_content': 'Lecture video text'}, start_time)

    def test_discussion_prompts(self):
        start_time = time.time()
        response = self.client.post('/api/llm/discussion_prompts', 
                                    data=json.dumps({'topic': 'Artificial Intelligence'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('prompts', data)
        self.log_test('/api/llm/discussion_prompts', response, {'topic': 'Artificial Intelligence'}, start_time)

    def test_interactive_quizzes(self):
        start_time = time.time()
        response = self.client.post('/api/llm/interactive_quizzes', 
                                    data=json.dumps({'lecture_content': 'Lecture content'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('quizzes', data)
        self.log_test('/api/llm/interactive_quizzes', response, {'lecture_content': 'Lecture content'}, start_time)

    def test_personalized_feedback(self):
        start_time = time.time()
        response = self.client.post('/api/llm/personalized_feedback', 
                                    data=json.dumps({'quiz_results': 'Good', 'assignment_results': 'Needs Improvement'}), 
                                    content_type='application/json')
        self.assertStatus(response, 200)
        data = json.loads(response.data)
        self.assertIn('feedback', data)
        self.log_test('/api/llm/personalized_feedback', response, {'quiz_results': 'Good', 'assignment_results': 'Needs Improvement'}, start_time)

if __name__ == '__main__':
    pytest.main()
