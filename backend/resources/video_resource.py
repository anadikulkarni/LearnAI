from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Video
from ..read_json_fields import video_fields
from flask_security import roles_required

class VideoResource(Resource):
    @marshal_with(video_fields)
    def get(self, video_id=None):
        if video_id is None:
            videos = Video.query.all()
            return videos
        else:
            video = Video.query.get(video_id)
            if video is not None:
                return video
            else:
                video_by_yt_id = Video.query.filter_by(yt_id=video_id).first()
                if video_by_yt_id is not None:
                    return video_by_yt_id
                else:
                    return {"message": "Video not found"}, 404
    # Sample curl command to get all videos:
    # curl -X GET http://localhost:5000/api/videos
    
    # Sample curl command to get a specific video by ID:
    # curl -X GET http://localhost:5000/api/videos/{video_id}

    @marshal_with(video_fields)
    @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        video = Video(**data)
        db.session.add(video)
        db.session.commit()
        return video, 201
    # Sample curl command to create a new video:
    # curl -X POST http://localhost:5000/api/videos \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "New Video",
    #            "url": "http://example.com/video",
    #            "course_id": 1
    #          }'

    @marshal_with(video_fields)
    @roles_required('admin', 'instructor')
    def put(self, video_id):
        video = Video.query.get_or_404(video_id)
        data = request.json
        for key, value in data.items():
            setattr(video, key, value)
        db.session.commit()
        return video
    # Sample curl command to update a specific video by ID:
    # curl -X PUT http://localhost:5000/api/videos/{video_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "title": "Updated Video Title",
    #            "url": "http://example.com/updated_video",
    #            "course_id": 2
    #          }'

    @roles_required('admin', 'instructor')
    def delete(self, video_id):
        video = Video.query.get_or_404(video_id)
        db.session.delete(video)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific video by ID:
    # curl -X DELETE http://localhost:5000/api/videos/{video_id}
