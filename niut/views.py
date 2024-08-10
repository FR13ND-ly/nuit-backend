from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Item
from django.core.files import File
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import getItemSerializer
from django.views import View
from django.utils.decorators import method_decorator
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

@method_decorator(csrf_exempt, name='dispatch')
class ItemsView(View):

    def get(self, request, *args, **kwargs):
        items = Item.objects.order_by('-date')
        res = []
        for item in items:
            res.append(getItemSerializer(item))
        return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)

    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files')
        res = []
        for file in files:
            image = Image.open(file)
            output = BytesIO()
            
            image.save(output, format='WebP', quality=20)
            
            webp_file = ContentFile(output.getvalue(), name=os.path.basename(file.name).split('.')[0] + '.webp')
            
            item = Item.objects.create(file=webp_file)
            item.save()
            
            res.append(getItemSerializer(item))
        return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)

    def delete(self, request, *args, **kwargs):
        item = get_object_or_404(Item, id=kwargs['id'])
        item.delete()
        return JsonResponse({}, status=status.HTTP_200_OK)
    

@csrf_exempt
def likeItem(request, id):
    item = get_object_or_404(Item, id=id)
    item = Item.objects.get(id=id)
    item.likes += 1
    item.save()
    return JsonResponse(item.likes, status=status.HTTP_200_OK, safe=False)