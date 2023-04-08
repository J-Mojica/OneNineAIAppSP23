from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import sklearn
import pandas as pd
import numpy as np
import pickle

from sklearn.linear_model import SGDRegressor, SGDClassifier


def retrain_model(request):

    with open('./users/'+request.user.username+'/model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    data = pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True)

    prediction_column = request.POST["feature1"]

    y = data[prediction_column]

    data.drop(prediction_column, axis=1, inplace=True)
    
    x = data
    
    
    
    model.partial_fit(x,y)

    model_pkl = pickle.dumps(model)

    with open('./users/'+request.user.username+'/model.pkl', 'wb') as model_file:
        model_file.write(model_pkl)

    response = HttpResponse(
                    model_pkl,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Disposition": 'attachment; filename="model.pkl"'
                    }
                )
    
    return response

def create_model(request):
    # print(list(request.POST.items()))

    

    data = pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True)

    if request.POST["model_type"] == "SGDRegressor":
        model = SGDRegressor()
    elif request.POST["model_type"] == "SGDClassifier":
        model = SGDClassifier()

    prediction_column = request.POST["feature1"]

    y = data[prediction_column]

    data.drop(prediction_column, axis=1, inplace=True)
    
    x = data
    
    
    model.fit(x,y)

    model_pkl = pickle.dumps(model)

    response = HttpResponse(
                    model_pkl,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Disposition": 'attachment; filename="model.pkl"'
                    }
                )

    with open('./users/'+request.user.username+'/model.pkl', 'wb') as model_file:
        model_file.write(model_pkl)
    
    return response