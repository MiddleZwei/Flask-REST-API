import unittest
import os
import json
from ..app import create_app, db


class Blogposts(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.blogpost = {
            "title": "test",
            "contents": "test"
        }

        self.user = {
            'name': 'Oliver',
            'email': 'oliver@gmail.com',
            'password': 'password123'
        }

        with self.app.app_context():
            # create all tables
            db.create_all()

    # / POST
    def test_blogpost_creation(self):
        self.create_a_user()

        res = self.client().post('/api/v1/blogposts/',
                                 headers={'Content-Type': 'application/json', 'api-token': self.api_token},
                                 data=json.dumps(self.blogpost)
                                 )
        json_data = json.loads(res.data)

        self.assertTrue(json_data.get('created_at'))
        self.assertEqual(res.status_code, 201)

    # / POST
    def test_unauthorized_blogpost_creation(self):
        self.create_a_user()

        res = self.client().post('/api/v1/blogposts/',
                                 headers={'Content-Type': 'application/json'},
                                 data=json.dumps(self.blogpost)
                                 )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    # / GET
    def test_get_all_blogposts(self):
        res = self.client().get('/api/v1/blogposts/',
                                headers={'Content-Type': 'application/json'}
                                )
        self.assertEqual(res.status_code, 200)

    # /id GET
    def test_get_blogpost(self):
        self.create_a_user()
        blogpost_json = self.create_blogpost()

        res = self.client().get('/api/v1/blogposts/' + str(blogpost_json.get('id')),
                                headers={'Content-Type': 'application/json'}
                                )

        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(json_data.get('created_at'))

    # /id PUT
    def test_update_blogpost(self):
        self.create_a_user()
        blogpost_json = self.create_blogpost()

        blogpost1 = {
            "title": "test1",
            "contents": "test1"
        }

        res = self.client().put('/api/v1/blogposts/' + str(blogpost_json.get('id')),
                                headers={'Content-Type': 'application/json', 'api-token': self.api_token},
                                data=json.dumps(blogpost1)
                                )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json_data.get('title'), 'test1')

    # /id PUT
    def test_update_unauthorized_blogpost(self):
        self.create_a_user()
        blogpost_json = self.create_blogpost()

        blogpost1 = {
            "title": "test1",
            "contents": "test1"
        }

        res = self.client().put('/api/v1/blogposts/' + str(blogpost_json.get('id')),
                                headers={'Content-Type': 'application/json'},
                                data=json.dumps(blogpost1)
                                )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    # /id DELETE
    def test_delete_blogpost(self):
        self.create_a_user()
        blogpost_json = self.create_blogpost()

        res = self.client().delete('/api/v1/blogposts/' + str(blogpost_json.get('id')),
                                   headers={'Content-Type': 'application/json', 'api-token': self.api_token}
                                   )

        self.assertEqual(res.status_code, 204)

    # /id DELETE
    def test_unauthorized_blogpost(self):
        self.create_a_user()
        blogpost_json = self.create_blogpost()

        res = self.client().delete('/api/v1/blogposts/' + str(blogpost_json.get('id')),
                                   headers={'Content-Type': 'application/json'}
                                   )
        json_data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue(json_data.get('error'))

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_a_user(self):
        self.user_res = self.client().post('/api/v1/users/',
                                           headers={'Content-Type': 'application/json'},
                                           data=json.dumps(self.user)
                                           )
        json_data = json.loads(self.user_res.data)

        self.api_token = json_data.get('jwt_token')

    def create_blogpost(self):
        blogpost_res = self.client().post('/api/v1/blogposts/',
                                          headers={'Content-Type': 'application/json', 'api-token': self.api_token},
                                          data=json.dumps(self.blogpost)
                                          )

        return json.loads(blogpost_res.data)


if __name__ == "__main__":
    unittest.main()
