import json

from django.shortcuts import render
from django.views     import View
from django.http      import JsonResponse

from .models          import Item
from core.utils       import authorization

# Create your views here.
class ItemView(View):
    @authorization
    def post(self, request):
        data  = json.loads(request.body)

        name  = data['name']
        price = data['price']
        image = data['image']

        Item.objects.create(
            name  = name,
            price = price,
            image = image,
        )

        return JsonResponse({'MESSAGE' : 'Items successfully added'}, status=400)