from flask_restful import fields
from sqlalchemy.orm import subqueryload
from datetime import datetime

class DateTime(fields.Raw):
    def format(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return value
    
course_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'category_id': fields.Integer,
    'instructor_id': fields.Integer,
    'youtube_playlist': fields.String,
    'image': fields.String,
    'created_at': DateTime,
    'updated_at': DateTime,
    'category': fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }),
    'instructor': fields.Nested({
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String
    }),
    'users': fields.List(fields.Nested({
        'id': fields.Integer,
        'username': fields.String,
        'email': fields.String
    })),
    'assignments': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })),
    'resources': fields.List(fields.Nested({
        'id': fields.Integer,
        'url': fields.String
    })),
    'videos': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'url': fields.String,
        'yt_id': fields.String
    })),
    'lecture_transcripts': fields.List(fields.Nested({
        'id': fields.Integer,
        'content': fields.String
    })),
    'ratings': fields.List(fields.Nested({
        'id': fields.Integer,
        'rating': fields.Float,
        'comment': fields.String,
        'user_id': fields.Integer
    })),
    'quizzes': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String
    })),
    'codingqs': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'ex_input': fields.String,
        'ex_output': fields.String,
    })),
}

category_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'courses': fields.List(fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    }))
}

assignment_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'course_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'course': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })
}

resource_fields = {
    'id': fields.Integer,
    'url': fields.String,
    'course_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'course': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })
}

video_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'url': fields.String,
    'course_id': fields.Integer,
    'yt_id': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'course': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })
}

lecture_transcript_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'course_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'course': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    }),
    'translations': fields.List(fields.Nested({
        'id': fields.Integer,
        'language': fields.String,
        'content': fields.String
    }))
}

translation_fields = {
    'id': fields.Integer,
    'language': fields.String,
    'content': fields.String,
    'lecture_transcript_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
}

assignment_feedback_fields = {
    'id': fields.Integer,
    'feedback': fields.String,
    'assignment_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'assignment': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })
}

quiz_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'course': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    }),
    'questions': fields.List(fields.Nested({
        'id': fields.Integer,
        'content': fields.String,
        'quiz_id': fields.Integer,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime,
        'options': fields.List(fields.Nested({
            'id': fields.Integer,
            'content': fields.String,
        }))
    })),
    'results': fields.List(fields.Nested({
        'id': fields.Integer,
        'score': fields.Float,
        'user_id': fields.Integer,
        'created_at': fields.DateTime
    }))
}

codingqs_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'ex_input': fields.String,
    'ex_output': fields.String,
    'course_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'course': fields.Nested({
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String
    })
}

question_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'quiz_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'quiz': fields.Nested({
        'id': fields.Integer,
        'title': fields.String
    }),
    'options': fields.List(fields.Nested({
        'id': fields.Integer,
        'content': fields.String,
        'is_correct': fields.Boolean
    }))
}

option_fields = {
    'id': fields.Integer,
    'content': fields.String,
    'is_correct': fields.Boolean,
    'question_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'question': fields.Nested({
        'id': fields.Integer,
        'content': fields.String
    })
}
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'active': fields.Boolean,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'is_admin': fields.Boolean,
    'roles': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String
    })),
    'courses': fields.List(fields.Nested(course_fields)),
    'quiz_results': fields.List(fields.Nested({
        'id': fields.Integer,
        'score': fields.Float,
        'quiz_id': fields.Integer
    }))
}

role_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}

course_rating_fields = {
    'id': fields.Integer,
    'rating': fields.Float,
    'comment': fields.String,
    'user_id': fields.Integer,
    'course_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'user': fields.Nested({
        'id': fields.Integer,
        'username': fields.String
    }),
    'course': fields.Nested(course_fields)
}

quiz_result_fields = {
    'id': fields.Integer,
    'score': fields.Float,
    'user_id': fields.Integer,
    'quiz_id': fields.Integer,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime
}
