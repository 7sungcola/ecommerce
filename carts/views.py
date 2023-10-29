import json

from django.http  import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError

from core.utils   import authorization
from .models      import Cart
from items.models import Item

class AddCartView(View):
    @authorization
    def get(self, request):
        user = request.user

        if not Cart.objects.filter(user_id=user.id).exists():
            return JsonResponse({'ERROR' : 'Cart does not exist'}, status=400)

        carts = Cart.objects.filter(user_id=user.id)

        cart_total = [{
            'cart_id' : cart.id,
            'item' : cart.quantity,
            'name' : cart.item.name,
            'price' : cart.item.price,
            'quantity' : cart.item.quantity,
            'image_url' : cart.item.image_url,
        } for cart in carts]

        return JsonResponse({'result' : cart_total}, status=200)

    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user
            user_id = user.id

            item_id = data['id']
            quantity = data['quantity']

            if Item.objects.filter(id=item_id):
                return JsonResponse({'MESSAGE' : 'Item does not exist'}, status=400)

            cart, created = Cart.objects.get_or_create(
                user_id = user_id,
                item_id = item_id,
            )

            cart.quantity += quantity
            cart.save()

            return JsonResponse({'MESSAGE' : 'SUCCESS'}, status=201)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)