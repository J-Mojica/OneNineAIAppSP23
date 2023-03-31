# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

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
from .forms import UploadFileForm
from .models import *
from .datacleanup import *

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template


        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))
    

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dataCleaning(request):
    if(request.method == 'POST'):
        if request.POST['method'] =='impute':
            return impute(request)
        if request.POST['method'] == 'dropFeature':
            return dropFeature(request)
        if request.POST['method'] == 'dropCorrelated':
            return dropCorrelated(request)
    return render(request, 'home/cleaning.html')

@login_required(login_url="/login/")
def modelMonitoring(request):
    # HERE GOES MLFLOW
    #model = sklearn.linear_model.LogisticRegression()
    #context = {'model': model}
    context = {'segment': 'monitoring'}
    return render(request, 'home/monitoring.html', context)

@login_required(login_url="/login/")
def modelReTraining(request):
    # HERE GOES RE-TRAINING

    context = {'segment': 'retraining'}
    return render(request, 'home/retraining.html', context)

@login_required(login_url="/login/")
def errorAnalysis(request):
    context = {'segment': 'errorAnalysis'}
    return render(request, 'home/errorAnalysis.html', context)

@login_required(login_url="/login/")
def useCases(request):
    # HERE GOES USE CASES

    context = {'segment': 'useCases'}
    return render(request, 'home/useCases.html', context)

@login_required(login_url="/login/")
def createModel(request):
    # HERE GOES CREATE MODEL

    context = {'segment': 'create'}
    return render(request, 'home/create.html', context)

# Create your views here.
def upload(request):
    file = request.FILES['fileUpload']
    fs=FileSystemStorage()
    #print("Working!")
    fs.save('./users/'+request.user.username+'/'+file.name,file) #saved into datasets folder
    # if we have enough time we could make a user based folder system like AFS
    #with open('diabetes.csv', 'wb+') as destination:
    #    for chunk in file.chunks():
    #        destination.write(chunk)
    return HttpResponse("Works!") #Just sending something that's ignored by jquery
