import json

from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse

from .models          import Item, Category
from core.utils       import authorization

# Create your views here.
class ItemView(View):
    def get(self, request):
        data = json.loads(request.body)

        name = data['name']

        item_found = Item.objects.get(name=name)

        return JsonResponse({'MESSAGE' : 'SUCCESS', 'RESULT' : item_found}, status=200)

    @authorization
    def post(self, request):
        data  = json.loads(request.body)

        category  = data['category']
        name      = data['name']
        price     = data['price']
        quantity  = data['quantity']
        image_url = data['image_url']

        category = Category.objects.get(name=category)

        # if Category.objects.exists(category):
        #     return JsonResponse({'ERROR' : 'Category already exists'}, status=400)

        Item.objects.create(
            category_id = category.id,
            name      = name,
            price     = price,
            quantity  = quantity,
            image_url = image_url,
        )

        return JsonResponse({'MESSAGE' : 'Items successfully added'}, status=200)
