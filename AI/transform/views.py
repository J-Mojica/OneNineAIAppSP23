from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import json as json
import numpy as np
# Create your views here.
def home(request):
    return render(request, 'transform/home.html')
def upload(request):
    file = request.FILES['fileUpload']
    fs=FileSystemStorage()
    fs.save('datasets/'+file.name,file) #saved into datasets folder
    # if we have enough time we could make a user based folder system like AFS
    #with open('diabetes.csv', 'wb+') as destination:
    #    for chunk in file.chunks():
    #        destination.write(chunk)
    return HttpResponse("Works!") #Just sending something that's ignored by jquery
def impute(request):
    df=pd.read_csv("datasets/"+request.POST['fileName'],skipinitialspace=True) #Turns all blank cells into NaN
    if(request.POST['feature1']=='All'):
        if(request.POST['imputeZero']=='Yes'): #Replace zeroes with NaNs for all if Yes
            df.replace(0,np.NaN,inplace=True)
        if(request.POST['imputeMethod']=='Median'):
            for col in df:
                try:
                    df[col].replace(np.NaN,df[col].median(),inplace=True)
                except:
                    df = df.fillna(df[col].value_counts().index[0])
        if(request.POST['imputeMethod']=='Mean'):
            for col in df:
                try:
                    df[col].replace(np.NaN,df[col].mean(),inplace=True)
                except:
                    df = df.fillna(df[col].value_counts().index[0])

    else:
        if(request.POST['imputeZero']=='Yes'): #Replace zeroes with NaNs for specific column if Yes
            try:
                df[request.POST['feature1']].replace(0,np.NaN,inplace=True)
            except:
                df = df.fillna(df[request.POST['feature1']].value_counts().index[0])
        if(request.POST['imputeMethod']=='Median'):
            try:
                df[request.POST['feature1']].replace(np.NaN,df[request.POST['feature1']].median(),inplace=True)
            except:
                df = df.fillna(df[request.POST['feature1']].value_counts().index[0])
        if(request.POST['imputeMethod']=='Mean'):
            try:
                df[request.POST['feature1']].replace(np.NaN,df[request.POST['feature1']].mean(),inplace=True)
            except:
                df = df.fillna(df[request.POST['feature1']].value_counts().index[0])
    df.to_csv('datasets/'+request.POST['fileName'],index=False)
    return HttpResponse(df.to_html())
def dropFeature(request):
    df=pd.read_csv("datasets/"+request.POST['fileName'],skipinitialspace=True)
    df.drop(request.POST['fileName'], axis=1,inplace=True)
    df.to_csv('datasets/'+request.POST['fileName'],index=False)
    return HttpResponse(df.to_html(classes='table table-stripped'))
#to bypass issues where we need to send multiple html things or html + other stuff
#Maybe you could store a temp html file and then GET request it from frontend
#Or you could append all wanted html things into one html file and parse through it in frontend
