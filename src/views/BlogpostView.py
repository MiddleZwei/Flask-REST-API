from flask import g, json, Blueprint, Response, request

from src.shared.funs import response
from ..shared.Authentication import Auth
from ..models.BlogpostModel import BlogpostModel, BlogpostSchema

# to group all endpoints in the same resource
blogpost_api = Blueprint('blogposts', __name__)

blogpost_schema = BlogpostSchema()


@blogpost_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data, error = blogpost_schema.load(req_data)
    if error:
        return response(error, 400)

    post = BlogpostModel(data)
    post.save()

    data = blogpost_schema.dump(post).data

    return response(data, 201)


@blogpost_api.route('/', methods=['GET'])
# @Auth.auth_required
def get_all_blogposts():
    blogposts = BlogpostModel.get_all_blogposts()
    serialized_data = blogpost_schema.dump(blogposts, many=True).data
    return response(serialized_data, 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['GET'])
# @Auth.auth_required
def get_blogpost(blogpost_id):
    blogpost = BlogpostModel.get_one_blogpost(blogpost_id)

    if not blogpost:
        response({'error': 'blogpost not found'}, 404)

    serialized_blogpost = blogpost_schema.dump(blogpost).data

    return response(serialized_blogpost, 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update_blogpost(blogpost_id):
    req_data = request.get_json()
    blogpost = BlogpostModel.get_one_blogpost(blogpost_id)

    if not blogpost:
        return response({'error': 'blogpost not found'}, 404)

    serialized_blogpost = blogpost_schema.dump(blogpost).data

    if serialized_blogpost.get('owner_id') != g.user.get('id'):
        return response({'error': 'permission denied'}, 401)

    # proceed with the updated blogpost's data if no error
    data, error = blogpost_schema.load(req_data, partial=True)

    if error:
        return response(error, 404)
    blogpost.update(data)

    serialized_blogpost = blogpost_schema.dump(blogpost).data

    return response(serialized_blogpost, 200)


@blogpost_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete_blogpost(blogpost_id):
    blogpost = BlogpostModel.get_one_blogpost(blogpost_id)

    if not blogpost:
        response({'error': 'blogpost not found'}, 404)
    serialized_blogpost = blogpost_schema.dump(blogpost).data

    if serialized_blogpost.get('owner_id') != g.user.get('id'):
        return response({'error': 'permission denied'}, 401)

    blogpost.delete()

    return response({'message': 'deleted'}, 204)
