import json, jwt

from datetime     import datetime

from django.test  import TestCase, Client

from my_settings  import SECRET_KEY, ALGORITHM
from items.models import Item, Category
from users.models import User
class ItemViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.name = 'test_item'

        self.user = User.objects.create(
            name='홍길동',
            email='test@naver.com',
            password='123456789!@',
        )

        Category.objects.create(
            id=1,
            name='test_category',
            thumbnail=''
        )

        Item.objects.create(
            category_id=1,
            name=self.name,
            price=99,
            quantity=100,
            image_url=''
        )

        self.token = jwt.encode({'id': self.user.id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Item.objects.all().delete()
        Category.objects.all().delete()

    def test_itemview_get_sucess(self):
        response = self.client.get(
            f'/items?name={self.name}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
{
            "MESSAGE": "SUCCESS",
            "RESULT": {
                "created_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                "modified_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                "category": 1,
                "name": self.name,
                "price": 99.0,
                "quantity": 100,
                "image_url": ""
            }
        })

    def test_create_success(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'category_id': 1,
            'name': 'test_item2',
            'price': 75,
            'quantity': 40,
            'image_url': ''
        }
        response = self.client.post(
            '/items', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE': 'Created'})

    def test_duplicate_item(self):
        headers = {'HTTP_Authorization': self.token}
        post = {
            'category_id': 1,
            'name': 'test_item',
            'price': 100,
            'quantity': 55,
            'image_url': ''
        }
        response = self.client.post(
            '/items', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR' : 'Item already exist'})

    def test_key_error(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'name': 'test_item2',
            'price': 35
        }
        response = self.client.post(
            '/items', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR': 'KEY_ERROR'})