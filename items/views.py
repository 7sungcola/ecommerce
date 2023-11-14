import json

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.core.serializers import serialize

from .models                import Item, Category, Review
from core.utils             import authorization

# Create your views here.
class ItemView(View):
    def get(self, request):
        try:
            name = request.GET.get('name', None)

            item_found = Item.objects.filter(name=name)

            serialized_data = serialize('json', item_found)
            serialized_data = json.loads(serialized_data)

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : serialized_data[0]['fields']}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

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

            return JsonResponse({'MESSAGE' : 'Created'}, status=201)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

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

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

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

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

class SearchItemView(View):
    def get(self, request):
        try:
            name = request.GET.get('name', None)

            result = Item.objects.filter(name__icontains=name)

            serialized_data = serialize('json', result)
            serialized_data = json.loads(serialized_data)

            return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : serialized_data[0]['fields']}, status=200)

        except ValidationError as e:
            return JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

class ReviewView(View):
    def get(self, request):
        try:
            name = request.GET.get('name', None)

            review_found = Review.objects.filter(item__name=name)

            serialized_data = serialize('json', review_found)
            serialized_data = json.loads(serialized_data)

            JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : serialized_data[0]['fields']})

        except ValidationError as e:
            JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)

    @authorization
    def post(self, request):
        try:
            data = json.loads(request.body)

            user = request.user

            body = data['body']

            name = request.GET.get('name', None)
            item = Item.objects.get(name=name)

            Review.objects.create(
                item = item,
                user = user,
                body = body
            )

            JsonResponse({'MESSAGE' : 'Created'}, status=201)

        except ValidationError as e:
            JsonResponse({'ERROR' : e.message}, status=400)

        except KeyError:
            return JsonResponse({'ERROR' : 'KEY_ERROR'}, status=400)