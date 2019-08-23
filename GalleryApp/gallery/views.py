from django.shortcuts import render
from django.template import loader
from django import forms
import gallery
from GalleryApp import settings
import os

# Create your views here.
def imggallery(request):

    image_list=[]
    static_dirs = settings.STATICFILES_DIRS
    for dir in static_dirs:
        imgpath = os.path.join(dir,'images')
        for file in os.listdir(imgpath):
            if file.endswith(".jpg"):
                image_list.append(settings.STATIC_URL+'images/'+file)
    # return HttpResponse('<h1>Hello</h1>')
    # template = loader.get_template('index.html')
    return render(request, 'gallery.html',context={'image_list':image_list})
