from django.shortcuts import render
from django.template import loader
from django import forms
from django.core.files.storage import FileSystemStorage 
from GalleryApp import settings
import os
import exifread
from base64 import b64encode



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
    return render(request, 'gallery.html',context={'allimages':allimages})


######################TODO######################
#Get exif data from user upload files


def exifupload(request): 
    if request.method == 'POST' and request.FILES['myfile']: 
        myfile = request.FILES['myfile']
        tags = exifread.process_file(myfile)
        exifvalues=[]
        for tag in tags.keys():
            if 'EXIF' in tag:
                tagname = str(tag).split(" ")[1]
            else:
                tagname = str(tag)
            exifvalues.append(tagname+" : "+str(tags[tag]))
        fs = FileSystemStorage(location='gallery/static/temp') 
        filename = fs.save(myfile.name, myfile)
        up_path=os.path.join('temp/', filename) 
        return render(request, 'exifdata.html', { 
                'exifvalues': exifvalues,
                'img' : up_path
        }) 
    print("hhh")
    return render(request, 'exifdata.html') 

#Add Get exif data for own pics
################################################

#Function to get exif data
def getexif(file):
    tags_list = ['EXIF FNumber',
                          'EXIF ExposureTime',
                          'EXIF ISOSpeedRatings',
                          'Image Model']

    with open(file,'rb') as img:
        tags = exifread.process_file(img)
        exifvalues=[]
        for tag in tags.keys():
            if tag in tags_list:
                if 'EXIF' in tag:
                    tagname = str(tag).split(" ")[1]
                else:
                    tagname = str(tag)
                exifvalues.append(tagname+" : "+str(tags[tag]))
        return exifvalues



#EXIF Upload page
def testexifupload(request):
    return render(request, 'exifdata.html',)
    