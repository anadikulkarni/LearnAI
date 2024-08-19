from flask import jsonify, request
from flask_restful import Resource, fields, marshal_with
from ..models import db, Category
from ..read_json_fields import category_fields
from ..post_json_fields import category_create_fields, category_update_fields
from flask_security import roles_required

class CategoryResource(Resource):
    @marshal_with(category_fields)
    def get(self, category_id=None):
        if category_id is None:
            categories = Category.query.all()
            return categories
        else:
            category = Category.query.get_or_404(category_id)
            return category
    # Sample curl command to get all categories:
    # curl -X GET http://localhost:5000/api/categories
    
    # Sample curl command to get a specific category by ID:
    # curl -X GET http://localhost:5000/api/categories/{category_id}

    @marshal_with(category_create_fields)
    # @roles_required('admin')
    def post(self):
        data = request.json
        print(data)
        category = Category(**data)
        db.session.add(category)
        db.session.commit()
        return category, 201
    # Sample curl command to create a new category:
    # curl -X POST http://localhost:5000/api/categories \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "name": "New Category",
    #            "description": "Category description"
    #          }'

    @marshal_with(category_update_fields)
    # @roles_required('admin')
    def put(self, category_id):
        category = Category.query.get_or_404(category_id)
        data = request.json
        for key, value in data.items():
            setattr(category, key, value)
        db.session.commit()
        return category
    # Sample curl command to update a specific category by ID:
    # curl -X PUT http://localhost:5000/api/categories/{category_id} \
    #      -H "Content-Type: application/json" \
    #      -d '{
    #            "name": "Updated Category",
    #            "description": "Updated description"
    #          }'

    # @roles_required('admin')
    def delete(self, category_id):
        category = Category.query.get_or_404(category_id)
        db.session.delete(category)
        db.session.commit()
        return '', 204
    # Sample curl command to delete a specific category by ID:
    # curl -X DELETE http://localhost:5000/api/categories/{category_id}
