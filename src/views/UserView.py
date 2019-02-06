from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def create():
    # create a user
    req_data = request.get_json()
    data, error = user_schema.load(req_data)

    if error:
        return response(error, 400)

    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return response(message, 400)

    # create and save
    user = UserModel(data)
    user.save()

    serialized_data = user_schema.dump(user).data

    token = Auth.generate_token(serialized_data.get('id'))

    return response({'jwt_token': token}, 201)


# Auth.auth_required decorator to validate the authenticity of the user requesting
@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    serialized_users = user_schema.dump(users, many=True).data
    return response(serialized_users, 200)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    # using partial=True since login doesn't require name field
    data, error = user_schema.load(req_data, partial=True)

    if error:
        return response(error, 400)

    if not data.get('email') or not data.get('password'):
        return response({'error': 'provide email and password to log in'}, 400)

    user = UserModel.get_user_by_email(data.get('email'))

    if not user:
        return response({'error': 'invalid credentials'}, 400)

    # validate the supplied password with the user's saved hash password
    if not user.check_hash(data.get('password')):
        return response({'error': 'invalid credentials'}, 400)

    serialized_data = user_schema.dump(user).data

    # this token then will be used in any subsequent request
    token = Auth.generate_token(serialized_data.get('id'))

    return response({'jwt_token': token}, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    user = UserModel.get_one_user(user_id)

    if not user:
        return response({'error': 'user not found'}, 404)

    serialized_user = user_schema.dump(user).data

    return response(serialized_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update_my_data():
    req_data = request.get_json()

    data, error = user_schema.load(req_data, partial=True)

    if error:
        return response(error, 400)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)

    serialized_user = user_schema.dump(user).data

    return response(serialized_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete_my_data():
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()

    return response({'message': 'deleted'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_my_data():

    user = UserModel.get_one_user(g.user.get('id'))
    serialized_user = user_schema.dump(user).data

    return response(serialized_user, 200)


def response(res, status_code):
    # response function
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
