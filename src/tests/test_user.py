import unittest
import os
import json
from ..app import create_app, db


class UsersTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.user = {
            'name': 'Oliver',
            'email': 'oliver@gmail.com',
            'password': 'password123'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    # / POST
    def test_user_creation(self):
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        json_data = json.loads(res.data)

        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 201)

    # / POST
    def test_user_creation_with_existing_email(self):
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)

        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    # / POST
    def test_user_creation_with_no_password(self):
        user2 = {
            'name': 'Oliver',
            'email': 'oliver@gmail.com'
        }

        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user2)
                                 )
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('password'))

    # / POST
    def test_user_creation_with_no_email(self):
        user2 = {
            'name': 'Oliver',
            'password': 'password123'
        }

        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user2)
                                 )
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('email'))

    # / POST
    def test_user_creation_with_empty_request(self):
        user2 = {}
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user2)
                                 )
        json_data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    # /login POST
    def test_user_login(self):
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        json_data = json.loads(res.data)
        self.assertTrue(json_data.get('jwt_token'))
        self.assertEqual(res.status_code, 200)

    # /login POST
    def test_user_login_with_invalid_password(self):
        user2 = {
            'password': 'wrongpassword',
            'email': 'oliver@mail.com',
        }
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)

        res = self.client().post('/api/v1/users/login',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user2)
                                 )
        json_data = json.loads(res.data)
        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    # /login POST
    def test_user_login_with_invalid_email(self):
        user2 = {
            'password': 'password123',
            'email': 'wrongemail@gmail.com',
        }
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v1/users/login',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(user2)
                                 )
        json_data = json.loads(res.data)

        self.assertFalse(json_data.get('jwt_token'))
        self.assertEqual(json_data.get('error'), 'invalid credentials')
        self.assertEqual(res.status_code, 400)

    # /me GET
    def test_user_get_me(self):
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)

        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().get('/api/v1/users/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token}
                                )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('email'), 'oliver@gmail.com')
        self.assertEqual(json_data.get('name'), 'Oliver')

    # /me PUT
    def test_user_update_me(self):
        user2 = {
            'name': 'new Oliver'
        }
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)

        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().put('/api/v1/users/me',
                                headers={'Content-Type': 'application/json', 'api-token': api_token},
                                data=json.dumps(user2)
                                )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('name'), 'new Oliver')

    # /me DELETE
    def test_delete_user(self):
        res = self.client().post('/api/v1/users/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.user)
                                 )
        self.assertEqual(res.status_code, 201)

        api_token = json.loads(res.data).get('jwt_token')
        res = self.client().delete('/api/v1/users/me',
                                   headers={'Content-Type': 'application/json', 'api-token': api_token}
                                   )
        self.assertEqual(res.status_code, 204)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
