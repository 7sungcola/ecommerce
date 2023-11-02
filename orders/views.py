import json
import uuid

from core.utils             import authorization
from carts.models           import Cart
from .models                import Order, OrderItem, OrderStatus

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import F, Sum
from django.core.exceptions import ValidationError

class OrderView(View):
    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user

            # user_id = user.id

            address = data['address']
            order_number = data['order_number']
            order_status = data['order_status']

            print(data)

            carts = Cart.objects.filter(
                user=user
            ).select_related(
                'item'
            ).annotate(
                price = Sum(F('item__quantity') * F('item__price'))
            )

            print(carts)

            total_price = carts.aggregate(
                total_price = Sum('price')
            )['total_price']

            print(total_price)

            order = Order(
                user    = user,
                address = address,
                order_number = uuid.uuid4(),
                order_status_id = OrderStatus.Status.PENDING
            )

            order_items = [
                OrderItem(
                    item = cart.item,
                    order = order,
                    quantity = cart.quantity
                ) for cart in carts
            ]

            carts.delete()

            order.order_status_id = OrderStatus.Status.COMPLETED
            order.save()

            OrderItem.objects.bulk_create(order_items)

            return JsonResponse({'MESSAGE' : 'Created'}, status=201)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)