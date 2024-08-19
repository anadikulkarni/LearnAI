from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from datetime import datetime

db = SQLAlchemy()

# Define the association table for roles and users
class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id'))

# Define the association table for enrollments
enrollments = db.Table('enrollments',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('course_id', db.Integer(), db.ForeignKey('courses.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    last_login = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    courses = db.relationship('Course', secondary=enrollments, back_populates='users')
    quiz_results = db.relationship('QuizResult', back_populates='user')

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    category_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    instructor_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    youtube_playlist = db.Column(db.String(255))  # Field to store YouTube playlist link
    image = db.Column(db.String(50000))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', back_populates='courses')
    instructor = db.relationship('User', back_populates='courses')
    users = db.relationship('User', secondary=enrollments, back_populates='courses')
    assignments = db.relationship('Assignment', back_populates='course')
    resources = db.relationship('Resource', back_populates='course')
    videos = db.relationship('Video', back_populates='course')  # Relationship with Video model
    lecture_transcripts = db.relationship('LectureTranscript', back_populates='course')
    ratings = db.relationship('CourseRating', back_populates='course')
    quizzes = db.relationship('Quiz', back_populates='course')  # Add this line to relate courses to quizzes
    codingqs = db.relationship('Codingqs', back_populates='course')



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    courses = db.relationship('Course', back_populates='category')

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    course = db.relationship('Course', back_populates='assignments')
    feedbacks = db.relationship('AssignmentFeedback', back_populates='assignment')

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer(), primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    course = db.relationship('Course', back_populates='resources')

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)  # New column added
    url = db.Column(db.String(255), nullable=False)
    yt_id = db.Column(db.String(255), nullable=False) # new column added for transcript
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    course = db.relationship('Course', back_populates='videos')

class LectureTranscript(db.Model):
    __tablename__ = 'lecture_transcripts'
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    course = db.relationship('Course', back_populates='lecture_transcripts')
    translations = db.relationship('Translation', back_populates='lecture_transcript')

class Translation(db.Model):
    __tablename__ = 'translations'
    id = db.Column(db.Integer(), primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    lecture_transcript_id = db.Column(db.Integer(), db.ForeignKey('lecture_transcripts.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    lecture_transcript = db.relationship('LectureTranscript', back_populates='translations')

class AssignmentFeedback(db.Model):
    __tablename__ = 'assignment_feedback'
    id = db.Column(db.Integer(), primary_key=True)
    feedback = db.Column(db.Text(), nullable=False)
    assignment_id = db.Column(db.Integer(), db.ForeignKey('assignments.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    assignment = db.relationship('Assignment', back_populates='feedbacks')

class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    id = db.Column(db.Integer(), primary_key=True)
    score = db.Column(db.Float(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='quiz_results')
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id'))
    quiz = db.relationship('Quiz', back_populates='results')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))  # Foreign key to relate quizzes to courses
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    questions = db.relationship('Question', back_populates='quiz')
    results = db.relationship('QuizResult', back_populates='quiz')
    course = db.relationship('Course', back_populates='quizzes')  # Add this line to relate quizzes to courses

class Codingqs(db.Model):
    __tablename__ = 'codingqs'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    ex_input = db.Column(db.Text(), nullable=False)
    ex_output = db.Column(db.Text(), nullable=False)
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))  # Foreign key to relate coding questions to courses
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    course = db.relationship('Course', back_populates='codingqs')  # Add this line to relate coding questions to courses

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.Text(), nullable=False)
    quiz_id = db.Column(db.Integer(), db.ForeignKey('quizzes.id'))
    quiz = db.relationship('Quiz', back_populates='questions')
    options = db.relationship('Option', back_populates='question')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer(), primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean(), default=False)
    question_id = db.Column(db.Integer(), db.ForeignKey('questions.id'))
    question = db.relationship('Question', back_populates='options')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

class CourseRating(db.Model):
    __tablename__ = 'course_ratings'
    id = db.Column(db.Integer(), primary_key=True)
    rating = db.Column(db.Float(), nullable=False)
    comment = db.Column(db.Text(), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer(), db.ForeignKey('courses.id'))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User')
    course = db.relationship('Course', back_populates='ratings')
