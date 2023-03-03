from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas
# Create your views here.
def home(request):
    return render(request, 'transform/home.html')
def upload(request):
    print("Testing")
    file = request.FILES['fileUpload']
    fs=FileSystemStorage()
    fs.save('datasets/'+file.name,file) #saved into datasets folder
    # if we have enough time we could make a user based folder system like AFS
    #with open('diabetes.csv', 'wb+') as destination:
    #    for chunk in file.chunks():
    #        destination.write(chunk)
    return HttpResponse("Works!") #Just sending something that's ignored by jquery