from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Item, Image
from django.core.files import File
from rest_framework import status
import os
from django.conf import settings
from django.shortcuts import get_object_or_404
from .serializers import getItemSerializer, getFileSerializer
from moviepy.editor import VideoFileClip
import io
from django.views import View
from django.utils.decorators import method_decorator
import tempfile


@method_decorator(csrf_exempt, name='dispatch')
class ItemsView(View):

    def get(self, request, *args, **kwargs):
        items = Item.objects.order_by('-date')
        res = []
        for item in items:
            res.append(getItemSerializer(item))
        return JsonResponse(res, status=status.HTTP_201_CREATED, safe=False)

    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        cover = Image.objects.get(id=data['cover'])
        if data.get('onhover') == 0:
            item = Item.objects.create(cover=cover)
        else:
            onhover = Image.objects.get(id=data['onhover'])
            item = Item.objects.create(cover=cover, onhover=onhover)
        item.save()
        return JsonResponse(getItemSerializer(item), status=status.HTTP_201_CREATED, safe=False)

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


@csrf_exempt
def uploadCover(request):
    image = Image.objects.create(file=File(request.FILES['cover'], name = request.FILES['cover'].name.split('.')[0] + '.jpg'))
    image.save()
    res = getFileSerializer(image)
    return JsonResponse(res, status=status.HTTP_200_OK)


@csrf_exempt
def uploadOnhover(request):
    video_file = request.FILES['onhover']
    video = VideoFileClip(video_file.temporary_file_path())

    temp_gif = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
    temp_gif_path = temp_gif.name
    try:
        video.write_gif(temp_gif_path, program='ffmpeg')
        temp_gif.close()
        
        with open(temp_gif_path, 'rb') as gif_file:
            output_filename = os.path.basename(video_file.name).split('.')[0] + ".gif"
            file_instance = Image.objects.create(file=File(gif_file, name=output_filename))
            file_instance.save()
    finally:
        if os.path.exists(temp_gif_path):
            os.remove(temp_gif_path)
    res = getFileSerializer(file_instance)
    return JsonResponse(res, status=status.HTTP_200_OK)