from flask_restful import Api
from .resources.user_resource import UserResource
from .resources.role_resource import RoleResource
from .resources.course_resource import CourseResource
from .resources.category_resource import CategoryResource
from .resources.assignment_resource import AssignmentResource
from .resources.assignmentfeedback_resource import AssignmentFeedbackResource
from .resources.resource_resource import ResourceResource
from .resources.transcript_resource import Transcript
from .resources.video_resource import VideoResource
from .resources.translation_resource import TranslationResource
from .resources.quiz_resource import QuizResource, SubmitQuizResource

from .resources.question_resource import QuestionResource
from .resources.option_resource import OptionResource
from .resources.quizresult_resource import QuizResultResource
from .resources.courserating_resource import CourseRatingResource
from .resources.genai_resources import SummarizeLecture,Chatbot,Feedback,Quiz,Translate,AnalyzeCode,RecommendCourses,HighlightSegments,DiscussionPrompts,InteractiveQuizzes,PersonalizedFeedback
from .resources.login_resource import LoginResource
from .resources.signup_resource import SignupResource
from .resources.logout_resource import LogoutResource
from .resources.coding_resource import CodingqsResource
from .resources.enrollment_resource import EnrollmentsResource


def create_api(app):
    api = Api(app, prefix='/api')

    # Add resources
    api.add_resource(UserResource, '/users', '/users/<int:user_id>')
    api.add_resource(RoleResource, '/roles', '/roles/<int:role_id>')
    api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>','/courses/category/<int:category_id>','/courses/search/<string:keyword>')
    api.add_resource(CategoryResource, '/categories', '/categories/<int:category_id>')
    api.add_resource(AssignmentResource, '/assignments', '/assignments/<int:assignment_id>')
    api.add_resource(AssignmentFeedbackResource, '/assignment_feedbacks', '/assignment_feedbacks/<int:feedback_id>', '/assignments/<int:assignment_id>/feedbacks')
    api.add_resource(ResourceResource, '/resources', '/resources/<int:resource_id>')
    api.add_resource(Transcript, '/transcript', '/transcript/<string:video_id>')
    api.add_resource(SubmitQuizResource, '/submit_quiz/<int:quiz_id>')

    # Login and SignUp refactored to api by Azfar
    api.add_resource(LoginResource, '/login')
    api.add_resource(SignupResource, '/signup')
    api.add_resource(LogoutResource, '/logout')

    
    # New resources
    api.add_resource(VideoResource, '/videos', '/videos/<string:video_id>')
    api.add_resource(TranslationResource, '/translations')
    api.add_resource(QuizResource, '/quizzes', '/quizzes/<int:quiz_id>',  '/quizzes/course/<int:course_id>')
    api.add_resource(QuestionResource, '/questions', '/questions/<int:quiz_id>', '/questions/quiz/<int:question_id>')
    api.add_resource(OptionResource, '/options', '/options/<int:option_id>', '/options/question/<int:question_id>') # For fetching options by question ID
    api.add_resource(QuizResultResource, '/quiz_results', '/quiz_results/<int:result_id>')
    api.add_resource(CourseRatingResource, '/course_ratings', '/course_ratings/<int:rating_id>')
    api.add_resource(CodingqsResource, '/codingqs', '/codingqs/<int:codingqs_id>', '/codingqs/course/<int:course_id>')
    api.add_resource(EnrollmentsResource, '/enrollments', '/enrollments/<int:user_id>', '/enrollments/course/<int:course_id>')

    
    #genai
    api.add_resource(SummarizeLecture, '/llm/summary')
    api.add_resource(Chatbot, '/llm/chatbot')
    api.add_resource(Feedback, '/llm/feedback')
    api.add_resource(Quiz, '/llm/quiz')
    api.add_resource(Translate, '/llm/translate')
    api.add_resource(AnalyzeCode, '/llm/analyze_code')
    api.add_resource(RecommendCourses, '/llm/recommend_courses')
    api.add_resource(HighlightSegments, '/llm/highlight_segments')
    api.add_resource(DiscussionPrompts, '/llm/discussion_prompts')
    api.add_resource(InteractiveQuizzes, '/llm/interactive_quizzes')
    api.add_resource(PersonalizedFeedback, '/llm/personalized_feedback')

    return api
