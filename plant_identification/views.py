# plant_identification/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .utils import identify_plant, get_image_data # Importing from the same directory

def index(request):
    return render(request, 'plant_identification/index.html')

from django.conf import settings

def identify_plant_view(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        api_key = settings.PLANT_ID_API_KEY
        plant_name, wikipedia_description = identify_plant(image.read(), api_key)
        
        # Assuming you have a function to get the URL of the uploaded image
        image_url = get_image_data(image)
        
        return render(request, 'plant_identification/result.html', {'plant_name': plant_name, 'wikipedia_description': wikipedia_description, 'image_url': image_url})
    else:
        return HttpResponse('Bad request')