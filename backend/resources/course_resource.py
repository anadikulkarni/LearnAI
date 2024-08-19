from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Course, Video, Quiz
from ..read_json_fields import course_fields
from ..post_json_fields import course_create_fields, course_update_fields
from flask_security import roles_required
from sqlalchemy.orm import subqueryload
from pytube import Playlist

class CourseResource(Resource):
    @marshal_with(course_fields)
    def get(self, course_id=None, category_id=None, keyword=None):
        if course_id:
            course = Course.query.options(
                subqueryload(Course.videos),
                subqueryload(Course.quizzes)
            ).get_or_404(course_id)
            return course
        elif category_id:
            courses = Course.query.filter_by(category_id=category_id).options(
                subqueryload(Course.videos),
                subqueryload(Course.quizzes)
            ).all()
            return courses
        elif keyword:
            search = f"%{keyword}%"
            courses = Course.query.filter(Course.title.ilike(search)).options(
                subqueryload(Course.videos),
                subqueryload(Course.quizzes)
            ).all()
            return courses
        else:
            courses = Course.query.options(
                subqueryload(Course.videos),
                subqueryload(Course.quizzes)
            ).all()
            return courses

    # Sample curl command to get all courses:
    # curl -X GET http://localhost:5000/api/courses
    
    # Sample curl command to get a specific course by ID:
    # curl -X GET http://localhost:5000/api/courses/{course_id}

    @marshal_with(course_create_fields)
    def post(self):
        data = request.json
        youtube_playlist = data.get('youtube_playlist', None)

        # Create and save the new course
        course = Course(**data)
        db.session.add(course)
        db.session.commit()

        # Get the course_id from the newly created course
        course_id = course.id

        def get_youtube_playlist_videos(playlist_url, course_id):
            playlist = Playlist(playlist_url)
            video_info = [
                {
                    "title": video.title,
                    "url": video.watch_url,
                    "yt_id": video.video_id,
                    "course_id": course_id
                }
                for video in playlist.videos
            ]
            return video_info

        try:
            if youtube_playlist:
                video_info = get_youtube_playlist_videos(youtube_playlist, course_id)
                print("YouTube Playlist Video Information:", video_info)

                # Add each video to the Video table
                for info in video_info:
                    video = Video(
                        title=info['title'],
                        url=info['url'],
                        yt_id=info['yt_id'],
                        course_id=info['course_id']
                    )
                    db.session.add(video)
                db.session.commit()

            else:
                print("No YouTube playlist URL provided.")
        except Exception as e:
            # Print or log the exception and continue
            print(f"Failed to fetch YouTube playlist videos: {e}")

        print(course.id)

        return course, 201

    # Sample curl command to create a new course:
    # curl -X POST http://localhost:5000/api/courses \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "New Course Title",
    #            "description": "Course description",
    #            "category_id": 1,
    #            "instructor_id": 1,
    #            "youtube_playlist": "http://youtube.com/playlist"
    #          }'

    @marshal_with(course_update_fields)
    # @roles_required('admin', 'instructor')
    def put(self, course_id):
        course = Course.query.get_or_404(course_id)
        data = request.json
        for key, value in data.items():
            setattr(course, key, value)
        db.session.commit()
        return course

    # Sample curl command to update a specific course by ID:
    # curl -X PUT http://localhost:5000/api/courses/{course_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "Updated Course Title",
    #            "description": "Updated description",
    #            "category_id": 2,
    #            "instructor_id": 2,
    #            "youtube_playlist": "http://youtube.com/updated-playlist"
    #          }'

    # @roles_required('admin', 'instructor')
    def delete(self, course_id):
        course = Course.query.get_or_404(course_id)
        db.session.delete(course)
        db.session.commit()
        return '', 204

    # Sample curl command to delete a specific course by ID:
    # curl -X DELETE http://localhost:5000/api/courses/{course_id}
    