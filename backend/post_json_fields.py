from flask_restful import fields

# Create and Update JSON Fields for Course
course_create_fields = {
    'title': fields.String,
    'description': fields.String,
    'category_id': fields.Integer,
    'instructor_id': fields.Integer,
    'youtube_playlist': fields.String,
    'image': fields.String
    
}

course_update_fields = {
    'title': fields.String,
    'description': fields.String,
    'category_id': fields.Integer,
    'instructor_id': fields.Integer,
    'youtube_playlist': fields.String,
    'image': fields.String
}

# Create and Update JSON Fields for Category
category_create_fields = {
    'name': fields.String
}

category_update_fields = {
    'name': fields.String
}

# Create and Update JSON Fields for Assignment
assignment_create_fields = {
    'title': fields.String,
    'description': fields.String,
    'course_id': fields.Integer
}

assignment_update_fields = {
    'title': fields.String,
    'description': fields.String
}

# Create and Update JSON Fields for Resource
resource_create_fields = {
    'url': fields.String,
    'course_id': fields.Integer
}

resource_update_fields = {
    'url': fields.String
}

# Create and Update JSON Fields for Video
video_create_fields = {
    'url': fields.String,
    'course_id': fields.Integer,
    'yt_id': fields.String
}

video_update_fields = {
    'url': fields.String,
    'yt_id': fields.String
}

# Create and Update JSON Fields for Lecture Transcript
lecture_transcript_create_fields = {
    'content': fields.String,
    'course_id': fields.Integer
}

lecture_transcript_update_fields = {
    'content': fields.String
}

# Create and Update JSON Fields for Translation
translation_create_fields = {
    'language': fields.String,
    'content': fields.String,
    'lecture_transcript_id': fields.Integer
}

translation_update_fields = {
    'language': fields.String,
    'content': fields.String
}

# Create and Update JSON Fields for Assignment Feedback
assignment_feedback_create_fields = {
    'feedback': fields.String,
    'assignment_id': fields.Integer
}

assignment_feedback_update_fields = {
    'feedback': fields.String
}

# Create and Update JSON Fields for Quiz
quiz_create_fields = {
    'title': fields.String,
    'course_id': fields.Integer
}

quiz_update_fields = {
    'title': fields.String
}

codingqs_create_fields = {
    'title': fields.String,
    'description': fields.String,
    'ex_input': fields.String,
    'ex_output': fields.String,
    'course_id': fields.Integer,
}

codingqs_update_fields = {
    'title': fields.String,
    'description': fields.String,
    'ex_input': fields.String,
    'ex_output': fields.String,
    'course_id': fields.Integer,
}

# Create and Update JSON Fields for Question
question_create_fields = {
    'content': fields.String,
    'quiz_id': fields.Integer
}

question_update_fields = {
    'content': fields.String
}

# Create and Update JSON Fields for Option
option_create_fields = {
    'content': fields.String,
    'is_correct': fields.Boolean,
    'question_id': fields.Integer
}

option_update_fields = {
    'content': fields.String,
    'is_correct': fields.Boolean
}

# Create and Update JSON Fields for User
user_create_fields = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'active': fields.Boolean
}

user_update_fields = {
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
    'active': fields.Boolean
}

# Create and Update JSON Fields for Role
role_create_fields = {
    'name': fields.String,
    'description': fields.String
}

role_update_fields = {
    'name': fields.String,
    'description': fields.String
}

# Create and Update JSON Fields for Course Rating
course_rating_create_fields = {
    'rating': fields.Float,
    'comment': fields.String,
    'user_id': fields.Integer,
    'course_id': fields.Integer
}

course_rating_update_fields = {
    'rating': fields.Float,
    'comment': fields.String
}
