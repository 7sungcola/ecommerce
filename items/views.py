import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from .models                import Item, Category
from core.utils             import authorization

# Create your views here.
class ItemView(View):
    def get(self, request):
        try:
            data = json.loads(request.body)

            name = data['name']

            item_found = Item.objects.get(name=name)

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : item_found}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

    @authorization
    def post(self, request):
        try:
            data  = json.loads(request.body)

            category_id = data['category_id']
            name        = data['name']
            price       = data['price']
            quantity    = data['quantity']
            image_url   = data['image_url']

            category = Category.objects.get(id=category_id)

            if Item.objects.filter(name=name).exists():
                return JsonResponse({'ERROR' : 'Item already exist'}, status=400)

            Item.objects.create(
                category_id = category.id,
                name        = name,
                price       = price,
                quantity    = quantity,
                image_url   = image_url,
            )

            return JsonResponse({'MESSAGE' : 'Created'}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

    @authorization
    def patch(self, request):
        try:
            data = json.loads(request.body)

            item_name = data['name']

            item = Item.objects.get(name=item_name)

            item.name      = data['name']
            item.price     = data['price']
            item.quantity  = data['quantity']
            item.image_url = data['image_url']

            item.save()

            return JsonResponse({'MESSAGE' : 'Updated'}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

    @authorization
    def delete(self, request):
        try:
            data = json.loads(request.body)

            item_name = data['name']

            item = Item.objects.filter(name=item_name)

            if item.exists():
                item.delete()

                return JsonResponse({'MESSAGE': 'Deleted'}, status=200)

            else:
                return JsonResponse({'ERROR': 'Item does not exist'}, status=400)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)