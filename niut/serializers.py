from django.conf import settings
import os 

def getItemSerializer(item):
    return {
        'id': item.id,
        'cover': settings.API_URL + "media/" + os.path.basename(item.file.file.name),
        'likes': item.likes,
        'date': item.date
    }