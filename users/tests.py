import json, jwt, bcrypt

from django.test  import TestCase, Client

from users.models import User
from my_settings  import SECRET_KEY, ALGORITHM

class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create(
            name='홍길동',
            email='test2@naver.com',
            password='123456789!@',
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_success(self):
        user = {
            'name': '홍홍길동',
            'email': 'test1@naver.com',
            'password': '123456789!@',
        }
        response = self.client.post(
            '/users/signUp', json.dumps(user), content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'Created'})

    def test_duplicated_user(self):
        user = {
            'name': '홍길동',
            'email': 'test2@naver.com',
            'password': '123456789!@',
        }
        response = self.client.post(
            '/users/signUp', json.dumps(user), content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR': 'Account already exists'})

    def test_email_format_error(self):
        user = {
            'name': '홍길동',
            'email': 'test3naver.com',
            'password': '123456789!@',
        }
        response = self.client.post(
            '/users/signUp', json.dumps(user), content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR': 'Email must contain @'})

    def test_password_format_error(self):
        user = {
            'name': '홍길동',
            'email': 'test4@naver.com',
            'password': '1234567',
        }
        response = self.client.post(
            '/users/signUp', json.dumps(user), content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR': 'Length of password needs to be longer than 8'})

    def test_key_error(self):
        user = {
            'name': '홍길동',
            'email': 'test5@naver.com',
        }
        response = self.client.post(
            '/users/signUp', json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR': 'KEY_ERROR'})

class SignInViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.token = jwt.encode({'id': 1}, SECRET_KEY, ALGORITHM)
        User.objects.create(
            name='홍길동',
            email='test2@naver.com',
            password=bcrypt.hashpw('123456789!@'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_login_success(self):
        user = {
            'email': 'test2@naver.com',
            'password': '123456789!@',
        }
        response = self.client.post(
            '/users/signIn', json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE': 'SUCCESS', 'TOKEN': self.token})