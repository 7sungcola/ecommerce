import json

from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse

from .models          import Item, Category
from core.utils       import authorization

# Create your views here.
class ItemView(View):
    @authorization
    def post(self, request):
        data  = json.loads(request.body)

        category = data['category']
        name     = data['name']
        price    = data['price']
        quantity = data['quantity']
        image    = data['image']

        category = Category.objects.get(name=category)

        Item.objects.create(
            category_id = category.id,
            name     = name,
            price    = price,
            quantity = quantity,
            image    = image,
        )

        return JsonResponse({'MESSAGE' : 'Items successfully added'}, status=400)