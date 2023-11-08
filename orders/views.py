import json, uuid

from core.utils             import authorization
from carts.models           import Cart
from .models                import Order, OrderItem, OrderStatus
from items.models           import Item

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

            address = data['address']

            carts = Cart.objects.filter(
                user=user
            ).select_related(
                'item'
            ).annotate(
                price = Sum(F('item__quantity') * F('item__price'))
            )

            order = Order(
                user            = user,
                address         = address,
                order_number    = str(uuid.uuid4()),
                order_status_id = OrderStatus.Status.PENDING
            )

            for cart in carts:
                order_items = [
                    OrderItem(
                        item=cart.item,
                        order=order,
                        quantity=cart.quantity
                    )
                ]
                item = Item.objects.get(id=cart.item.id)
                item.quantity = F('quantity') - cart.quantity
                item.save()

            carts.delete()

            order.order_status_id = OrderStatus.Status.COMPLETED
            order.save()

            OrderItem.objects.bulk_create(order_items)

            return JsonResponse({'MESSAGE' : 'Created'}, status=201)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

    @authorization
    def get(self, request, **kwargs):
        try:
            user = request.user

            order_id = kwargs['order_id']

            order = Order.objects.get(user=user, id=order_id)

            order_item = OrderItem.objects.filter(
                order=order
            ).select_related(
                'item'
            ).annotate(
                price=Sum(F('item__quantity') * F('item__price'))
            )

            total_price = order_item.aggregate(
                total_price=Sum('price')
            )['total_price']

            result = {
                'name' : user.name,
                'address' : order.address,
                'order_number' : order.order_number,
                'total_price' : total_price,
                'order_item' : [
                    {
                        'item' : order_item.item.name,
                        'quantity' : order_item.quantity,
                        'price' : order_item.item.price
                    } for order_item in order.orderitem_set.all()
                ]
            }

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : result}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)