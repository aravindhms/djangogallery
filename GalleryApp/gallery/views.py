from django.shortcuts import render
from django.template import loader
from django import forms
import gallery

# Create your views here.
def imggallery(request):
    # return HttpResponse('<h1>Hello</h1>')
    # template = loader.get_template('index.html')
    return render(request, 'index.html')
