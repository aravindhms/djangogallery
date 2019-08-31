from django.shortcuts import render
from django.core.files.storage import FileSystemStorage 
from GalleryApp import settings
import os
import exifread
from base64 import b64encode
import copy



# Get a list of all '.jpg' files from specified directory and display as gallery including basic exif details
def imggallery(request):
    allimages={}
    static_dirs = settings.STATICFILES_DIRS
    for imdir in static_dirs:
        imgpath = os.path.join(imdir,'images')
        for file in os.listdir(imgpath):
            if file.endswith(".jpg"):
                fileurl=settings.STATIC_URL+"images/"+file
                exifdata = getexif(os.path.join(imgpath,file))
                allimages.update({fileurl : exifdata})
    return render(request, 'gallery.html',context={'allimages':allimages})


######################TODO######################
#Display exif data from user upload files


def exifupload(request): 
    if request.method == 'POST' and request.FILES['upfile']: 
        myfile = copy.deepcopy(request.FILES['upfile'])
        encoded = b64encode(request.FILES['upfile'].read()).decode('ascii')
        mime = "image/jpeg"
        uri = "data:%s;base64,%s" % (mime, encoded)
        
        print(myfile.size)
        tags = exifread.process_file(myfile)
        print()
        exifvalues=[]
        for exiftag in tags.keys():
            
            if 'EXIF' in exiftag:
                tagname = str(exiftag).split(" ")[1]
            else:
                tagname = str(exiftag)
            exifvalues.append(tagname+" : "+str(tags[exiftag]))
        return render(request, 'exifdata.html', { 
                'exifvalues': exifvalues,
                'img' : uri
        }) 
    print("hhh")
    return render(request, 'exifdata.html') 


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
    