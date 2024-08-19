from flask import jsonify, request
from flask_restful import Resource
from youtube_transcript_api import YouTubeTranscriptApi
from ..models import db, LectureTranscript
from flask_security import roles_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime

class Transcript(Resource):
    # @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        video_id = data.get('video_id')
        course_id = data.get('course_id')

        if not video_id or not course_id:
            return {"error": "video_id and course_id are required"}, 400

        try:
            # Fetch transcript from YouTube
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Extract only the text from each transcript entry
            text_only = " ".join([entry['text'] for entry in transcript])
            print(text_only)
            # Create and save the transcript to the database
            new_transcript = LectureTranscript(
                content=text_only,
                course_id=course_id
            )
            print(new_transcript)
            db.session.add(new_transcript)
            db.session.commit()
            print(type(text_only), text_only)
            return {"message": "Transcript added successfully", "transcript": text_only}, 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid course_id or other integrity issue"}, 400
        except Exception as e:
            return {"error": str(e)}, 500


    def get(self, video_id):
        try:
            # Retrieve course_id from request arguments
            course_id = request.args.get('course_id')
            
            if not course_id:
                return {"error": "course_id is required"}, 400

            # Try to get the transcript from the database
            transcript_record = LectureTranscript.query.filter_by(content=video_id, course_id=course_id).first()

            if transcript_record:
                # If transcript exists in the database, return it
                return {"transcript": transcript_record.content}

            # If not in the database, fetch from YouTube API
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            # Extract only the text from each transcript entry
            text_only = " ".join([entry['text'] for entry in transcript])
            
            # Save the fetched transcript to the database
            new_transcript = LectureTranscript(
                content=text_only,
                course_id=course_id
            )
            db.session.add(new_transcript)
            db.session.commit()

            return {"transcript": text_only}

        except Exception as e:
            return {"error": str(e)}, 500
    
    # @roles_required('admin', 'instructor')
    def put(self, video_id):
        data = request.json
        transcript_record = LectureTranscript.query.filter_by(content=video_id).first()

        if not transcript_record:
            return {"error": "Transcript not found"}, 404

        new_content = data.get('content')
        new_course_id = data.get('course_id', transcript_record.course_id)

        if new_content:
            transcript_record.content = new_content
        transcript_record.course_id = new_course_id
        transcript_record.updated_at = datetime.utcnow()

        try:
            db.session.commit()
            return {"message": "Transcript updated successfully", "transcript": transcript_record.content}, 200
        except IntegrityError:
            db.session.rollback()
            return {"error": "Invalid course_id or other integrity issue"}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    # @roles_required('admin')
    def delete(self, video_id):
        transcript_record = LectureTranscript.query.filter_by(content=video_id).first()

        if not transcript_record:
            return {"error": "Transcript not found"}, 404

        try:
            db.session.delete(transcript_record)
            db.session.commit()
            return {"message": "Transcript deleted successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
