from django.conf import settings
import os 

def getItemSerializer(item):
    return {
        'id': item.id,
        'cover': getFileSerializer(item.cover),
        'onhover': getFileSerializer(item.onhover),
        'likes': item.likes,
        'date': item.date
    }

def getFileSerializer(file):
    if file:
        return {
            'id': file.id,
            'url': settings.API_URL + "media/" + os.path.basename(file.file.name)
        }
    else:
        return {
            'id': 0,
            'url': ""
        }