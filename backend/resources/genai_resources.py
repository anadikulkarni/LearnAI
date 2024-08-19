from flask import jsonify, request, make_response
from flask_restful import Resource
from flask_security import roles_required
from ..models import User,Course
import ollama
import json

# Define the model name
# MODEL_NAME = 'llama3.1
MODEL_NAME = 'gemma2:2b'

# Function to call the Ollama API directly
def call_ollama_model(prompt, stream=True):
    stream_response = ollama.chat(
        model=MODEL_NAME,
        messages=[{'role': 'user', 'content': prompt}],
        stream=stream,
    )
    if stream:
        result = ''
        for chunk in stream_response:
            print(chunk['message']['content'], end='', flush=True)
            result += chunk['message']['content']
        return result
    else:
        # Assuming you want to handle non-streaming responses differently if necessary
        return stream_response.get('message', {}).get('content', '')

class SummarizeLecture(Resource):
    def post(self):
        data = request.get_json()
        transcript = data.get('transcript')
        prompt = f"Summarize the following lecture transcript.Provide a short and concise response: {transcript}"
        summary = call_ollama_model(prompt)
        return jsonify({"summary": summary})

class Chatbot(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        prompt = f"Answer the following question.Provide a short response: {query}"
        answer = call_ollama_model(prompt)
        return jsonify({"answer": answer})

class Feedback(Resource):
    def post(self):
        data = request.get_json()
        code = data.get('code')
        error = data.get('error')
        prompt = f"Provide short feedback on the following code that produced the error '{error}': {code}"
        feedback = call_ollama_model(prompt)
        return jsonify({"feedback": feedback})

class Quiz(Resource):
    def post(self):
        data = request.get_json()
        topic = data.get('topic')
        prompt = f"Generate a set of quiz questions for the topic (no more than 5): {topic}"
        quiz_questions = call_ollama_model(prompt)
        return jsonify({"questions": quiz_questions})

class Translate(Resource):
    def post(self):
        data = request.get_json()
        transcript = data.get('transcript')
        language = data.get('language')
        # prompt = f"Translate the following lecture transcript in the respective script of the language.Provide a accurate response with no other information other than the translation in the response:  {language}: {transcript}"
        prompt = f"Translate the following lecture transcript to {language}. Provide a accurate response with no other information other than the translation in the response: {transcript}"
        print(prompt)
        translation = call_ollama_model(prompt)
        return jsonify({"translation": translation})

class AnalyzeCode(Resource):
    def post(self):
        data = request.get_json()
        code = data.get('code')
        prompt = f"Analyze the following code and suggest improvements based on industry standards. Provide a short response: {code}"
        analysis = call_ollama_model(prompt)
        return jsonify({"analysis": analysis})

class RecommendCourses(Resource):
    def post(self):
        # Initialize response data dictionary
        response_data = {"recommendations": None, "error": None}
        
        # Debugging: Print the received request data
        data = request.get_json()
        user_id = data.get('user_id')
        if user_id is None:
            response_data["error"] = "No user_id provided"
        else:
            # Fetch the user from the database
            try:
                user = User.query.filter_by(id=user_id).first()
                if not user:
                    response_data["error"] = "User not found"
                else:
                    # Calculate performance based on quiz results
                    quiz_results = user.quiz_results
                    if quiz_results:
                        average_score = sum([result.score for result in quiz_results]) / len(quiz_results)
                        performance = f"Average quiz score: {average_score:.2f}"
                    else:
                        performance = "No quiz results available"
                    # Derive interests based on enrolled courses
                    interests = ", ".join([course.title for course in user.courses]) if user.courses else "No enrollments"
                    # Fetch all available courses
                    available_courses = Course.query.all()
                    available_course_titles = ", ".join([course.title for course in available_courses])
                    # Generate the prompt for recommendations
                    prompt = f"Based on the following performance and interests, recommend relevant courses. \
                    Provide a short response: {performance}, {interests}. Available courses are: {available_course_titles}"
                    # Call the Ollama model to get recommendations
                    try:
                        recommendations = call_ollama_model(prompt)
                        response_data["recommendations"] = recommendations
                    except Exception as e:
                        response_data["error"] = f"Error generating recommendations: {str(e)}"
            except Exception as e:
                response_data["error"] = f"Error querying the database: {str(e)}"
        # Return response with 200 OK status
        return make_response(jsonify(response_data), 200)


class HighlightSegments(Resource):
    def post(self):
        data = request.get_json()
        video_content = data.get('video_content')
        prompt = f"Highlight key segments in the following video content: {video_content}"
        highlights = call_ollama_model(prompt)
        return jsonify({"highlights": highlights})

class DiscussionPrompts(Resource):
    def post(self):
        data = request.get_json()
        topic = data.get('topic')
        prompt = f"Generate short discussion prompts for the topic: {topic}"
        prompts = call_ollama_model(prompt)
        return jsonify({"prompts": prompts})

class InteractiveQuizzes(Resource):
    def post(self):
        data = request.get_json()
        lecture_content = data.get('lecture_content')
        
        prompt = """Generate interactive quiz questions (no more than 5) for the following lecture topic. Respond with a json output, example: [{"question":"abcd", "options":[a,b,c,d], correct_option_index:1},{"question":"efgh", "options":[a,b,c,d], correct_option_index:3}]:""" + lecture_content
        
        quizzes_response = call_ollama_model(prompt)
        
        # Extract JSON string between the first "[" and the last "]"
        start_idx = quizzes_response.find('[')
        end_idx = quizzes_response.rfind(']') + 1  # +1 to include the closing bracket
        
        if start_idx != -1 and end_idx != -1:
            quizzes_json_str = quizzes_response[start_idx:end_idx]
            quizzes = json.loads(quizzes_json_str)
        else:
            quizzes = []
        
        return jsonify({"quizzes": quizzes})

class PersonalizedFeedback(Resource):
    def post(self):
        data = request.get_json()
        quiz_results = data.get('quiz_results')
        assignment_results = data.get('assignment_results')
        prompt = f"Provide a short personalized feedback based on the following quiz and assignment results: {quiz_results}, {assignment_results}"
        feedback = call_ollama_model(prompt)
        return jsonify({"feedback": feedback})
