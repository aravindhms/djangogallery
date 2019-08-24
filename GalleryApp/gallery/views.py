from django.shortcuts import render
from django.template import loader
from django import forms
from GalleryApp import settings
import os
import exifread

# Get a list of all '.jpg' files from specified directory
def imggallery(request):
    allimages={}
    static_dirs = settings.STATICFILES_DIRS
    for dir in static_dirs:
        imgpath = os.path.join(dir,'images')
        for file in os.listdir(imgpath):
            if file.endswith(".jpg"):
                fileurl=settings.STATIC_URL+"images/"+file
                exifdata = getexif(os.path.join(imgpath,file))
                allimages.update({fileurl : exifdata})
    print(allimages)
    return render(request, 'gallery.html',context={'allimages':allimages})


######################TODO######################
#Get exif data from user upload files
#Add Get exif data for own pics
################################################

#Function to get exif data
def getexif(file):
    tags_list = ['EXIF Aperture',
                          'EXIF ExposureTime',
                          'EXIF ISOSpeedRatings',
                          'Image Model']

    with open(file,'rb') as img:
        tags = exifread.process_file(img)
        exifvalues=[]
        for tag in tags.keys():
            if tag in tags_list:
                exifvalues.append(str(tag)+" : "+str(tags[tag]))
        return exifvalues
    # print(exifdata)