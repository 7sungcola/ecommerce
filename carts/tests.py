import json, jwt

from django.test  import TestCase, Client

from my_settings  import SECRET_KEY, ALGORITHM
from items.models import Item, Category
from carts.models import Cart
from users.models import User
class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user = User.objects.create(
            id=1,
            name='홍길동',
            email='test@naver.com',
            password='123456789!@',
        )

        Category.objects.create(
            id=1,
            name='test_category',
            thumbnail=''
        )

        self.item = Item.objects.create(
            id=1,
            category_id=1,
            name='test_item',
            price=99,
            quantity=120,
            image_url=''
        )

        self.item2 = Item.objects.create(
            id=2,
            category_id=1,
            name='test_item2',
            price=125,
            quantity=50,
            image_url=''
        )

        Cart.objects.create(
            user=self.user,
            item=self.item,
            quantity=50
        )

        self.token = jwt.encode({'id': self.user.id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()
        Item.objects.all().delete()
        Category.objects.all().delete()
        Cart.objects.all().delete()

    def test_create_success(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'id': self.item2.id,
            'quantity': 50
        }
        response = self.client.post(
            '/carts', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'MESSAGE' : 'Created'})

    def test_update_success(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'id': self.item.id,
            'quantity': 50
        }
        response = self.client.post(
            '/carts', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'MESSAGE': 'Updated'})

    def test_item_does_not_exist(self):
        headers = {'HTTP_Authorization': self.token}
        post = {
            'id': 35,
            'quantity': 50
        }
        response = self.client.post(
            '/carts', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR' : 'Item does not exist'})

    def test_item_stock_unavailable(self):
        headers = {'HTTP_Authorization': self.token}
        post = {
            'id': self.item.id,
            'quantity': 500
        }
        response = self.client.post(
            '/carts', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR' : 'Item stock unavailable'})

    def test_key_error(self):
        headers = {'HTTP_Authorization' : self.token}
        post = {
            'name': 'test_item2',
            'price': 35
        }
        response = self.client.post(
            '/carts', json.dumps(post), content_type="application/json", **headers
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'ERROR' : 'KEY_ERROR'})