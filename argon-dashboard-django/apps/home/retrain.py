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

from sklearn.linear_model import SGDRegressor, SGDClassifier, LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor


def retrain_model(request):

    with open('./users/'+request.user.username+'/model_dict.pkl', 'rb') as model_file:
        model_dict = pickle.load(model_file)

    new_data = pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True)

    if list(new_data.columns) != model_dict["features"]:
        return HttpResponse("")

    model = model_dict["model"]
    # prediction_column = request.POST["feature1"]
    prediction_column = model_dict["prediction_column"]

    if model_dict["retrainable"] == True:

        y = new_data[prediction_column]

        new_data.drop(prediction_column, axis=1, inplace=True)
        
        x = new_data

        model.fit(x,y)

    elif model_dict["retrainable"] == False:

        ds_list = []

        for ds in model_dict["model_ds"]:
            ds_list.append(pd.read_csv('./users/'+request.user.username+'/'+ds,skipinitialspace=True))
        
        ds_list.append(new_data)

        data = pd.concat(ds_list)

        y = data[prediction_column]

        data.drop(prediction_column, axis=1, inplace=True)

        x = data

        model.fit(x,y)
    
    model_dict["model"] = model
    model_dict["model_ds"].append(request.POST['fileName'])

    model_pkl = pickle.dumps(model_dict)

    with open('./users/'+request.user.username+'/model_dict.pkl', 'wb') as model_file:
        model_file.write(model_pkl)

    response = HttpResponse(
                    model_pkl,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Disposition": 'attachment; filename="model_dict.pkl"'
                    }
                )
    
    return response

def create_model(request):

    data = pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True)
    retrainable = False

    features = list(data.columns)

    if request.POST["model_type"] == "SGDRegressor":
        model = SGDRegressor()
        retrainable = True
    elif request.POST["model_type"] == "SGDClassifier":
        model = SGDClassifier()
        retrainable = True
    elif request.POST["model_type"] == "LogisticRegression":
        model = LogisticRegression()
        retrainable = False
    elif request.POST["model_type"] == "LinearRegression":
        model = LinearRegression()
        retrainable = False
    elif request.POST["model_type"] == "DecisionTreeClassifier":
        model = DecisionTreeClassifier()
        retrainable = False
    elif request.POST["model_type"] == "DecisionTreeRegressor":
        model = DecisionTreeRegressor()
        retrainable = False
    else:
        return HttpResponse("")

    prediction_column = request.POST["feature1"]

    y = data[prediction_column]

    data.drop(prediction_column, axis=1, inplace=True)
    
    x = data
    
    
    model.fit(x,y)

    model_dict = {
                    "model_type": request.POST["model_type"],
                    "prediction_column": prediction_column,
                    "features": features,
                    "model": model,
                    "retrainable": retrainable,
                    "model_ds": [request.POST['fileName']]
                }

    model_pkl = pickle.dumps(model_dict)

    response = HttpResponse(
                    model_pkl,
                    headers={
                        "Content-Type": "application/octet-stream",
                        "Content-Disposition": 'attachment; filename="model_dict.pkl"'
                    }
                )

    with open('./users/'+request.user.username+'/model_dict.pkl', 'wb') as model_file:
        model_file.write(model_pkl)
    
    return response