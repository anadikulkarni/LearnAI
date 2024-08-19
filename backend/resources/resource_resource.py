from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Resource as CourseResource
from ..read_json_fields import resource_fields
from flask_security import roles_required

class ResourceResource(Resource):
    @marshal_with(resource_fields)
    def get(self, resource_id=None):
        if resource_id is None:
            resources = CourseResource.query.all()
            return resources
        else:
            resource = CourseResource.query.get_or_404(resource_id)
            return resource
    # Sample curl command to get all resources:
    # curl -X GET http://localhost:5000/api/resources
    
    # Sample curl command to get a specific resource by ID:
    # curl -X GET http://localhost:5000/api/resources/{resource_id}

    @marshal_with(resource_fields)
    # @roles_required('admin', 'instructor')
    def post(self):
        data = request.json
        resource = CourseResource(**data)
        db.session.add(resource)
        db.session.commit()
        return resource, 201
    # Sample curl command to create a new resource:
    # curl -X POST http://localhost:5000/api/resources \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "url": "http://example.com/resource",
    #            "course_id": 1
    #          }'

    @marshal_with(resource_fields)
    # @roles_required('admin', 'instructor')
    def put(self, resource_id):
        resource = CourseResource.query.get_or_404(resource_id)
        data = request.json
        for key, value in data.items():
            setattr(resource, key, value)
        db.session.commit()
        return resource
    # Sample curl command to update a specific resource by ID:
    # curl -X PUT http://localhost:5000/api/resources/{resource_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "url": "http://example.com/updated-resource",
    #            "course_id": 2
    #          }'

    # @roles_required('admin', 'instructor')
    def delete(self, resource_id):
        resource = CourseResource.query.get_or_404(resource_id)
        db.session.delete(resource)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific resource by ID:
    # curl -X DELETE http://localhost:5000/api/resources/{resource_id}
