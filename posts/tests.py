import json, jwt

from django.test  import TestCase, Client

from my_settings  import SECRET_KEY, ALGORITHM
from posts.models import Post
from users.models import User
# Create your tests here.
class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        User.objects.create(
            name='홍길동2',
            email='test2@naver.com',
            password='123456789!@2',
        )

        self.user = User.objects.create(
            name='홍길동',
            email='test@naver.com',
            password='123456789!@',
        )

        Post.objects.create(
            title='Test for post',
            body='hello this is test code for post view heuh',
            user_id=self.user.id
        )

        self.token = jwt.encode({'id': self.user.id}, SECRET_KEY, ALGORITHM)
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()

    def test_create_success(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'title': 'Test for post2',
            'body': 'hello this is test code for post view heuh heuh heuh',
        }
        response = self.client.post(
            '/posts/post', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'Created'})

    def test_key_error(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'title':'Test for post',
        }
        response = self.client.post(
            '/posts/post', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR': 'KEY_ERROR'})

