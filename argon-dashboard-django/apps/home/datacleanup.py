from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import json as json
import numpy as np
#Any datacleanup stuff goes here: (Pass in the raw request from the view)
def impute(request):

    df=pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True) #Turns all blank cells into NaN
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
    df.to_csv('./users/'+request.user.username+'/'+request.POST['fileName'],index=False)
    return HttpResponse(df.to_html(classes='dataframe table table-striped table-bordered dataTable no-footer'))

def dropFeature(request):
    print(request.POST)
    df=pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True)
    df.drop(request.POST['feature2'], axis=1,inplace=True)
    df.to_csv('./users/'+request.user.username+'/'+request.POST['fileName'],index=False)
    return HttpResponse(df.to_html(classes='dataframe table table-striped table-bordered dataTable no-footer'))

def dropCorrelated(request):
    print(request.POST)
    df=pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True)
    cor_matrix = df.corr().abs()
    upper_tri = cor_matrix.where(np.triu(np.ones(cor_matrix.shape),k=1).astype(np.bool))
    to_drop = [column for column in upper_tri.columns if (column!=request.POST["target"]) and any(upper_tri[column] > float(request.POST["corrThreshold"]))]
    print(to_drop)
    df.drop(columns=to_drop, axis=1,inplace=True)
    df.to_csv('./users/'+request.user.username+'/'+request.POST['fileName'],index=False)
    return HttpResponse(df.to_html(classes='dataframe table table-striped table-bordered dataTable no-footer'))

#def dropOutlier(request):
    

#to bypass issues where we need to send multiple html things or html + other stuff
#Maybe you could store a temp html file and then GET request it from frontend
#Or you could append all wanted html things into one html file and parse through it in frontend
